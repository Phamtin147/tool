// LMS Universal AutoPilot Pro - Content Script
// Author: Amtia / Phamtin147 (https://github.com/Phamtin147)

(function () {
  'use strict';

  if (window.__LMS_AUTOPILOT_LOADED__) return;
  window.__LMS_AUTOPILOT_LOADED__ = true;

  let isSolving = false;
  let shouldStop = false;

  // Configuration defaults
  const config = {
    geminiApiKey: '',
    geminiModel: 'gemini-flash-latest',
    solvingMode: 'stealth', // 'stealth' or 'autoclick'
    humanDelay: 2.0
  };

  async function loadConfig() {
    return new Promise((resolve) => {
      chrome.storage.local.get(['geminiApiKey', 'geminiModel', 'solvingMode', 'humanDelay'], (res) => {
        if (res.geminiApiKey) config.geminiApiKey = res.geminiApiKey;
        if (res.geminiModel) config.geminiModel = res.geminiModel;
        if (res.solvingMode) config.solvingMode = res.solvingMode;
        if (res.humanDelay) config.humanDelay = parseFloat(res.humanDelay) || 2.0;
        resolve(config);
      });
    });
  }

  // Detect quiz elements on current page
  function detectQuizQuestions() {
    const questions = [];

    // 1. Canvas LMS
    const canvasItems = document.querySelectorAll('.question.quiz_sortable, .question_holder, .display_question');
    if (canvasItems.length > 0) {
      canvasItems.forEach((el, idx) => {
        const textEl = el.querySelector('.question_text, .text');
        const qText = textEl ? textEl.innerText.trim() : '';
        const choices = [];
        el.querySelectorAll('.answer, .answers .answer_label').forEach((ansEl) => {
          const input = ansEl.querySelector('input[type="radio"], input[type="checkbox"]') || ansEl.closest('label')?.querySelector('input');
          const label = ansEl.innerText.trim();
          if (label) choices.push({ label, element: ansEl, input });
        });
        if (qText && choices.length > 0) {
          questions.push({ id: `canvas_${idx}`, container: el, text: qText, choices });
        }
      });
      if (questions.length > 0) return { type: 'Canvas', questions };
    }

    // 2. Moodle LMS
    const moodleItems = document.querySelectorAll('.que.multichoice, .que.truefalse, .que');
    if (moodleItems.length > 0) {
      moodleItems.forEach((el, idx) => {
        const textEl = el.querySelector('.qtext');
        const qText = textEl ? textEl.innerText.trim() : '';
        const choices = [];
        el.querySelectorAll('.answer > div, .answer label').forEach((ansEl) => {
          const input = ansEl.querySelector('input[type="radio"], input[type="checkbox"]') || (ansEl.tagName === 'LABEL' ? document.getElementById(ansEl.htmlFor) : null);
          const label = ansEl.innerText.trim();
          if (label) choices.push({ label, element: ansEl, input });
        });
        if (qText && choices.length > 0) {
          questions.push({ id: `moodle_${idx}`, container: el, text: qText, choices });
        }
      });
      if (questions.length > 0) return { type: 'Moodle', questions };
    }

    // 3. Google Forms
    const googleFormItems = document.querySelectorAll('div[role="listitem"]');
    if (googleFormItems.length > 0) {
      googleFormItems.forEach((el, idx) => {
        const titleEl = el.querySelector('div[role="heading"]');
        const qText = titleEl ? titleEl.innerText.trim() : '';
        const choices = [];
        el.querySelectorAll('div[role="radio"], div[role="checkbox"]').forEach((ansEl) => {
          const label = ansEl.innerText.trim() || ansEl.getAttribute('aria-label') || '';
          if (label) choices.push({ label, element: ansEl, input: ansEl });
        });
        if (qText && choices.length > 0) {
          questions.push({ id: `gform_${idx}`, container: el, text: qText, choices });
        }
      });
      if (questions.length > 0) return { type: 'Google Forms', questions };
    }

    // 4. Blackboard / Generic LMS fallback
    const genericItems = document.querySelectorAll('.takeQuestionDiv, fieldset, [class*="question-item"], [class*="quiz-question"]');
    genericItems.forEach((el, idx) => {
      const qText = el.innerText.split('\n')[0].trim();
      const choices = [];
      el.querySelectorAll('label, .answer, [class*="option"]').forEach((ansEl) => {
        const input = ansEl.querySelector('input[type="radio"], input[type="checkbox"]');
        const label = ansEl.innerText.trim();
        if (label && label.length < 300) choices.push({ label, element: ansEl, input });
      });
      if (qText && choices.length >= 2) {
        questions.push({ id: `generic_${idx}`, container: el, text: qText, choices });
      }
    });

    return { type: questions.length > 0 ? 'Generic LMS' : 'None', questions };
  }

  // Call Gemini API to solve a question
  async function callGemini(qText, choices) {
    await loadConfig();
    if (!config.geminiApiKey) {
      throw new Error('Chưa nhập Gemini API Key trong Popup Extension!');
    }

    const choicesFormatted = choices
      .map((c, i) => `[${String.fromCharCode(65 + i)}] ${c.label}`)
      .join('\n');

    const prompt = `Solve this multiple-choice question. Return ONLY the letter of the correct choice (e.g. A, B, C, D) followed by a short justification:\n\nQuestion:\n${qText}\n\nChoices:\n${choicesFormatted}\n\nOutput format:\nCORRECT: <Letter>\nREASON: <1 short sentence>`;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${config.geminiModel}:generateContent?key=${config.geminiApiKey}`;
    const payload = {
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.1, maxOutputTokens: 150 }
    };

    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error(err.error?.message || `Lỗi API: HTTP ${resp.status}`);
    }

    const data = await resp.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
    const match = text.match(/CORRECT:\s*([A-Za-z])/i);
    if (match) {
      const charCode = match[1].toUpperCase().charCodeAt(0);
      const index = charCode - 65;
      return { index, raw: text };
    }
    return { index: 0, raw: text };
  }

  // Highlight or select answer
  function applyAnswer(questionObj, chosenIndex) {
    if (chosenIndex < 0 || chosenIndex >= questionObj.choices.length) return;
    const target = questionObj.choices[chosenIndex];

    if (config.solvingMode === 'autoclick') {
      if (target.input) {
        target.input.click();
      } else if (target.element) {
        target.element.click();
      }
    }

    // Apply visual indicator (Stealth underline / green dot)
    if (target.element) {
      target.element.style.position = 'relative';
      target.element.style.borderBottom = '2px dashed #10b981';
      target.element.style.borderRadius = '4px';

      let dot = target.element.querySelector('.lms-autopilot-dot');
      if (!dot) {
        dot = document.createElement('span');
        dot.className = 'lms-autopilot-dot';
        dot.style.cssText = 'display:inline-block;width:6px;height:6px;background:#10b981;border-radius:50%;margin-left:6px;vertical-align:middle;';
        target.element.appendChild(dot);
      }
    }
  }

  // Create In-Page Floating HUD Widget
  function injectHUD() {
    if (document.getElementById('lms-autopilot-hud')) return;

    const hud = document.createElement('div');
    hud.id = 'lms-autopilot-hud';
    hud.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 2147483647;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 12px 16px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 13px;
      width: 260px;
      user-select: none;
      transition: all 0.3s ease;
    `;

    hud.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; cursor:move;" id="lms-hud-header">
        <strong style="color:#38bdf8; display:flex; align-items:center; gap:6px;">
          <span>⚡</span> LMS AutoPilot
        </strong>
        <span id="lms-hud-type" style="font-size:10px; background:#1e293b; color:#94a3b8; padding:2px 6px; border-radius:4px;">Detecting...</span>
      </div>
      <div id="lms-hud-status" style="font-size:11px; color:#cbd5e1; margin-bottom:10px; min-height:16px;">
        Sẵn sàng quét câu hỏi...
      </div>
      <div style="display:flex; flex-direction:column; gap:6px;">
        <button id="lms-btn-scan" style="background:#0284c7; color:#fff; border:none; padding:7px 10px; border-radius:6px; font-weight:600; cursor:pointer;">
          🔍 Quét & Giải Đề Này
        </button>
        <button id="lms-btn-stop" style="background:#475569; color:#fff; border:none; padding:6px 10px; border-radius:6px; font-size:11px; cursor:pointer; display:none;">
          ⏹️ Dừng lại
        </button>
      </div>
    `;

    document.body.appendChild(hud);

    // Initial detection
    const info = detectQuizQuestions();
    const typeBadge = document.getElementById('lms-hud-type');
    const statusText = document.getElementById('lms-hud-status');

    if (info.questions.length > 0) {
      typeBadge.textContent = `${info.type} (${info.questions.length}Q)`;
      typeBadge.style.color = '#38bdf8';
      statusText.textContent = `Tìm thấy ${info.questions.length} câu hỏi.`;
    } else {
      typeBadge.textContent = 'No Quiz';
      statusText.textContent = 'Không tìm thấy câu hỏi trắc nghiệm.';
    }

    // Attach button handlers
    const btnScan = document.getElementById('lms-btn-scan');
    const btnStop = document.getElementById('lms-btn-stop');

    btnScan.addEventListener('click', async () => {
      if (isSolving) return;
      isSolving = true;
      shouldStop = false;
      btnScan.style.display = 'none';
      btnStop.style.display = 'block';

      try {
        await loadConfig();
        const detected = detectQuizQuestions();
        if (detected.questions.length === 0) {
          statusText.textContent = 'Không có câu hỏi nào để giải.';
          return;
        }

        for (let i = 0; i < detected.questions.length; i++) {
          if (shouldStop) break;
          const q = detected.questions[i];
          statusText.textContent = `Đang giải câu ${i + 1}/${detected.questions.length}...`;

          try {
            const answer = await callGemini(q.text, q.choices);
            applyAnswer(q, answer.index);
          } catch (err) {
            console.error('LMS Solve Error:', err);
            statusText.textContent = `Lỗi câu ${i + 1}: ${err.message}`;
          }

          // Human delay
          const delayMs = (config.humanDelay + Math.random() * 0.8) * 1000;
          await new Promise((r) => setTimeout(r, delayMs));
        }

        statusText.textContent = shouldStop ? 'Đã dừng giải.' : '✓ Hoàn thành tất cả câu hỏi!';
      } catch (e) {
        statusText.textContent = `Lỗi: ${e.message}`;
      } finally {
        isSolving = false;
        btnScan.style.display = 'block';
        btnStop.style.display = 'none';
      }
    });

    btnStop.addEventListener('click', () => {
      shouldStop = true;
      statusText.textContent = 'Đang dừng...';
    });
  }

  // Inject when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectHUD);
  } else {
    injectHUD();
  }
})();
