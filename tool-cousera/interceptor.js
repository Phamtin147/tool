// Coursera AutoPilot Pro - AI Grader Blocker & Anti-Cheat Interceptor
// Injected at document_start in MAIN world to intercept network and DOM before page scripts run

(() => {
  if (window.__COURSERA_AI_BLOCKER_INSTALLED__) return;
  window.__COURSERA_AI_BLOCKER_INSTALLED__ = true;

  console.log("[Coursera AutoPilot] AI Grader & Anti-Lockout Interceptor active.");

  // 0. Anti-Cheat / Exam Lockout Defeater & Focus Spoofing
  try {
    // Spoof visibility & focus state so exam scripts never detect tab switches or blur
    Object.defineProperty(document, "hidden", { get: () => false, configurable: true });
    Object.defineProperty(document, "visibilityState", { get: () => "visible", configurable: true });
    Object.defineProperty(document, "webkitVisibilityState", { get: () => "visible", configurable: true });
    document.hasFocus = () => true;

    // Block anti-cheat event listeners (visibilitychange, blur, focusout, pagehide, mouseleave)
    const blockedEvents = new Set([
      "visibilitychange",
      "webkitvisibilitychange",
      "blur",
      "focusout",
      "mouseleave",
      "mouseout",
      "pagehide"
    ]);

    const rawAddEventListener = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function (type, listener, options) {
      if (this === window || this === document || this === document.body) {
        if (blockedEvents.has(String(type).toLowerCase())) {
          return; // Neutralize anti-cheat listener
        }
      }
      return rawAddEventListener.call(this, type, listener, options);
    };

    // Unblock right-click, copy, paste, select, cut
    const unblockHandler = (e) => {
      e.stopImmediatePropagation();
    };
    ["contextmenu", "copy", "cut", "paste", "selectstart"].forEach((evt) => {
      window.addEventListener(evt, unblockHandler, true);
      document.addEventListener(evt, unblockHandler, true);
    });
  } catch (e) {
    console.error("[Coursera AutoPilot] Anti-cheat spoofing error:", e);
  }

  // 1. Inject immediate CSS to hide AI grader elements permanently
  const injectStyle = () => {
    if (document.getElementById("coursera-ai-killer-style")) return;
    const style = document.createElement("style");
    style.id = "coursera-ai-killer-style";
    style.textContent = `
      .rc-AIGradeInstruction,
      .css-8h7v9a,
      .rc-AiFeedbackContainer,
      .rc-AiReviewContainer,
      [data-testid*="ai-grade"],
      [data-testid*="ai-grading"],
      [data-testid*="ai-evaluator"],
      [data-testid*="ai-evaluation"],
      [data-testid*="ai-feedback"],
      [data-testid*="ai-review"],
      [data-testid*="ai-coach"],
      [class*="AIGrade"],
      [class*="AiGrading"],
      [class*="ai-grading"],
      [class*="AiReview"],
      [class*="ai-feedback"],
      [class*="ai-coach"],
      [class*="ai-evaluation"],
      div[id*="ai-grader"],
      div[id*="ai-grading"],
      div[aria-label*="AI grading"],
      div[aria-label*="AI Graded"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
      }
    `;
    (document.head || document.documentElement).appendChild(style);
  };

  injectStyle();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectStyle);
  }

  // 2. Intercept window.fetch to block AI evaluation and force HUMAN grading
  const rawFetch = window.fetch;
  window.fetch = async function (input, init) {
    let url = "";
    if (typeof input === "string") {
      url = input;
    } else if (input && input.url) {
      url = input.url;
    }

    const lowerUrl = url.toLowerCase();

    // Check if URL is an AI grader evaluation endpoint
    const isAiEvaluationEndpoint =
      lowerUrl.includes("aigrading") ||
      lowerUrl.includes("ai-grader") ||
      lowerUrl.includes("ai_grader") ||
      lowerUrl.includes("ai-evaluation") ||
      lowerUrl.includes("aifeedback") ||
      lowerUrl.includes("ai-feedback") ||
      lowerUrl.includes("evaluatewithai") ||
      lowerUrl.includes("gradewithai");

    // Check if disabled flag is set or always active
    const isAiDisabled =
      localStorage.getItem("coursera_disable_ai_grader") === "true" ||
      sessionStorage.getItem("coursera_disable_ai_grader") === "true";

    if (isAiDisabled && isAiEvaluationEndpoint) {
      console.warn("[Coursera AutoPilot] Blocked AI evaluation fetch to:", url);
      return new Response(JSON.stringify({ status: "BLOCKED_BY_AUTOPILOT", message: "AI grading disabled" }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Rewrite submission requests to enforce HUMAN grading
    if (init && init.body && typeof init.body === "string") {
      if (
        lowerUrl.includes("ondemandpeersubmissions.v1") ||
        lowerUrl.includes("ondemandpeersubmissiondrafts.v1") ||
        lowerUrl.includes("graphql")
      ) {
        try {
          if (init.body.includes('"gradingType"') || init.body.includes('"useAi"')) {
            let bodyStr = init.body;
            bodyStr = bodyStr.replace(/"gradingType"\s*:\s*"(AI|AUTO|AUTOMATED)"/gi, '"gradingType":"HUMAN"');
            bodyStr = bodyStr.replace(/"useAiGrader"\s*:\s*true/gi, '"useAiGrader":false');
            bodyStr = bodyStr.replace(/"useAi"\s*:\s*true/gi, '"useAi":false');
            init.body = bodyStr;
            console.log("[Coursera AutoPilot] Enforced HUMAN grading on outgoing request to:", url);
          }
        } catch {}
      }
    }

    return rawFetch.apply(this, arguments);
  };

  // 3. Intercept XMLHttpRequest to block AI evaluation and force HUMAN grading
  const rawXhrOpen = XMLHttpRequest.prototype.open;
  const rawXhrSend = XMLHttpRequest.prototype.send;

  XMLHttpRequest.prototype.open = function (method, url) {
    this._url = String(url || "");
    this._method = method;
    return rawXhrOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function (body) {
    const lowerUrl = (this._url || "").toLowerCase();
    const isAiEvaluationEndpoint =
      lowerUrl.includes("aigrading") ||
      lowerUrl.includes("ai-grader") ||
      lowerUrl.includes("ai_grader") ||
      lowerUrl.includes("ai-evaluation") ||
      lowerUrl.includes("aifeedback") ||
      lowerUrl.includes("ai-feedback") ||
      lowerUrl.includes("evaluatewithai") ||
      lowerUrl.includes("gradewithai");

    const isAiDisabled =
      localStorage.getItem("coursera_disable_ai_grader") === "true" ||
      sessionStorage.getItem("coursera_disable_ai_grader") === "true";

    if (isAiDisabled && isAiEvaluationEndpoint) {
      console.warn("[Coursera AutoPilot] Blocked AI evaluation XHR to:", this._url);
      Object.defineProperty(this, "responseText", { value: '{"status":"BLOCKED"}' });
      Object.defineProperty(this, "status", { value: 200 });
      Object.defineProperty(this, "readyState", { value: 4 });
      this.dispatchEvent(new Event("load"));
      return;
    }

    if (body && typeof body === "string") {
      if (
        lowerUrl.includes("ondemandpeersubmissions.v1") ||
        lowerUrl.includes("ondemandpeersubmissiondrafts.v1")
      ) {
        try {
          body = body.replace(/"gradingType"\s*:\s*"(AI|AUTO|AUTOMATED)"/gi, '"gradingType":"HUMAN"');
          body = body.replace(/"useAiGrader"\s*:\s*true/gi, '"useAiGrader":false');
          body = body.replace(/"useAi"\s*:\s*true/gi, '"useAi":false');
        } catch {}
      }
    }

    return rawXhrSend.apply(this, [body]);
  };

  // 4. Auto-click "Switch to peer grading" whenever it appears in DOM
  const checkAndOptOut = () => {
    if (
      localStorage.getItem("coursera_disable_ai_grader") !== "true" &&
      sessionStorage.getItem("coursera_disable_ai_grader") !== "true"
    ) {
      return;
    }

    const clickables = Array.from(
      document.querySelectorAll("button, a, [role='button'], input[type='button'], span[role='button']")
    );

    for (const el of clickables) {
      const txt = (el.innerText || el.textContent || el.getAttribute("aria-label") || "").toLowerCase().trim();
      if (
        txt.includes("switch to peer") ||
        txt.includes("peer grading instead") ||
        txt.includes("opt out of ai") ||
        txt.includes("chuyển sang chấm") ||
        txt.includes("đánh giá ngang hàng")
      ) {
        try {
          console.log("[Coursera AutoPilot] Auto-clicking Switch to Peer:", txt);
          el.click();
          setTimeout(() => {
            const confirmBtns = Array.from(document.querySelectorAll("[role='dialog'] button, .cds-modal button"));
            for (const cb of confirmBtns) {
              const cTxt = (cb.innerText || cb.textContent || "").toLowerCase();
              if (cTxt.includes("switch") || cTxt.includes("confirm") || cTxt.includes("xác nhận") || cTxt.includes("yes")) {
                cb.click();
                console.log("[Coursera AutoPilot] Auto-confirmed switch in modal.");
              }
            }
          }, 300);
        } catch {}
      }
    }
  };

  // Run observer on DOM changes
  const observer = new MutationObserver(() => {
    injectStyle();
    checkAndOptOut();
  });

  observer.observe(document.documentElement, { childList: true, subtree: true });
})();
