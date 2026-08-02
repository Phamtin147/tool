const SPEED_VALUES = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4];
const NOTICE_ID = "manual-video-controller-notice";

const SKIP_BUTTON_ID = "manual-video-controller-skip-button";
const SUBMIT_BUTTON_ID = "manual-video-controller-submit-button";

function styleFloatingButton(button, bottom, background) {
  button.style.position = "fixed";
  button.style.right = "16px";
  button.style.bottom = bottom;
  button.style.zIndex = "2147483647";
  button.style.padding = "10px 14px";
  button.style.border = "0";
  button.style.borderRadius = "999px";
  button.style.background = background;
  button.style.color = "#fff";
  button.style.font = "600 14px/1.2 system-ui, sans-serif";
  button.style.boxShadow = "0 8px 24px rgba(0, 0, 0, 0.28)";
  button.style.cursor = "pointer";
}

function ensureSkipButton() {
  if (document.getElementById(SKIP_BUTTON_ID)) {
    return;
  }

  const button = document.createElement("button");
  button.id = SKIP_BUTTON_ID;
  button.type = "button";
  button.textContent = "Auto Skip";
  styleFloatingButton(button, "64px", "#e11d48");

  button.addEventListener("click", () => {
    if (autoSkipRunning) {
      autoSkipRunning = false;
      button.textContent = "Auto Skip";
      showNotice("Auto skip stopping...");
      return;
    }

    autoSkipRunning = true;
    button.textContent = "Stop Skip";
    skipCourseContinuously().finally(() => {
      autoSkipRunning = false;
      button.textContent = "Auto Skip";
    });
  });

  document.documentElement.appendChild(button);
}

function ensureSubmitButton() {
  if (document.getElementById(SUBMIT_BUTTON_ID)) {
    return;
  }

  const button = document.createElement("button");
  button.id = SUBMIT_BUTTON_ID;
  button.type = "button";
  button.textContent = "Auto Submit";
  styleFloatingButton(button, "112px", "#2563eb");

  button.addEventListener("click", () => {
    autoSubmitQuiz();
  });

  document.documentElement.appendChild(button);
}

const observedVideos = new WeakSet();
let lastActiveVideo = null;
let autoSkipRunning = false;

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function isVisibleElement(element) {
  const rect = element.getBoundingClientRect();
  const style = window.getComputedStyle(element);
  return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
}

function findVideo() {
  const videos = Array.from(document.querySelectorAll("video")).filter(isVisibleElement);

  if (videos.length === 0) {
    lastActiveVideo = null;
    return null;
  }

  if (lastActiveVideo && videos.includes(lastActiveVideo)) {
    return lastActiveVideo;
  }

  const playingVideo = videos.find((video) => !video.paused && !video.ended);
  lastActiveVideo = playingVideo || videos[0];
  return lastActiveVideo;
}

function nearestSpeed(currentRate, direction, settings) {
  const allowedValues = SPEED_VALUES.filter((rate) => rate >= settings.minSpeed && rate <= settings.maxSpeed);

  if (direction > 0) {
    return allowedValues.find((rate) => rate > currentRate + 0.01) || settings.maxSpeed;
  }

  return [...allowedValues].reverse().find((rate) => rate < currentRate - 0.01) || settings.minSpeed;
}

function getVisibleClickables(root = document) {
  const selector = [
    "a[href]",
    "button",
    "[role='button']",
    "[role='link']",
    "[tabindex]:not([tabindex='-1'])"
  ].join(", ");

  return Array.from(root.querySelectorAll(selector)).filter(isVisibleElement);
}

function goToNextCourseItem() {
  const clickables = getVisibleClickables();
  const nextTextPattern = /(next|tiếp|kế tiếp|bài tiếp|sau)/i;
  const explicitNext = clickables.find((element) => {
    const label = [element.textContent, element.getAttribute("aria-label"), element.getAttribute("title")]
      .filter(Boolean)
      .join(" ");
    return nextTextPattern.test(label) && !element.disabled && element.getAttribute("aria-disabled") !== "true";
  });

  if (explicitNext) {
    explicitNext.click();
    return true;
  }

  const activeSelector = [
    "[aria-current='page']",
    "[aria-current='true']",
    "[data-active='true']",
    "[data-selected='true']",
    ".active",
    ".selected",
    ".current"
  ].join(", ");
  const activeElement = document.querySelector(activeSelector) || clickables.find((element) => {
    if (!(element instanceof HTMLAnchorElement)) {
      return false;
    }

    return element.href === window.location.href || element.hash === window.location.hash;
  });

  if (!activeElement) {
    return false;
  }

  const sidebar = activeElement.closest("aside, nav, [role='navigation'], [class*='sidebar'], [class*='sider'], [class*='menu'], [class*='lesson'], [class*='course'], [class*='playlist']") || document;
  const sidebarClickables = getVisibleClickables(sidebar);
  const activeClickable = activeElement.matches("a[href], button, [role='button'], [role='link'], [tabindex]:not([tabindex='-1'])")
    ? activeElement
    : activeElement.querySelector("a[href], button, [role='button'], [role='link'], [tabindex]:not([tabindex='-1'])") || activeElement.closest("a[href], button, [role='button'], [role='link'], [tabindex]:not([tabindex='-1'])");
  const currentIndex = sidebarClickables.findIndex((element) => element === activeClickable || element.contains(activeElement) || activeElement.contains(element));

  if (currentIndex === -1) {
    return false;
  }

  const nextClickable = sidebarClickables.slice(currentIndex + 1).find((element) => {
    const text = element.textContent.trim();
    return text.length > 0 && !element.disabled && element.getAttribute("aria-disabled") !== "true";
  });

  if (!nextClickable) {
    return false;
  }

  nextClickable.scrollIntoView({ block: "center", inline: "nearest" });
  nextClickable.click();
  return true;
}

function getActiveCourseItemText() {
  const activeSelector = [
    "[aria-current='page']",
    "[aria-current='true']",
    "[data-active='true']",
    "[data-selected='true']",
    ".active",
    ".selected",
    ".current"
  ].join(", ");
  const activeElement = document.querySelector(activeSelector);

  if (!activeElement) {
    return "";
  }

  const item = activeElement.closest("li, [role='listitem'], a[href], button, [class*='item'], [class*='lesson'], [class*='module']") || activeElement;
  return item.textContent.replace(/\s+/g, " ").trim();
}

function isActiveQuizItem() {
  return /(quiz|assessment|question|exam|test|câu hỏi|bài kiểm tra|kiểm tra)/i.test(getActiveCourseItemText());
}

function sleep(milliseconds) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

function getPageSignature() {
  return document.body.innerText.replace(/\s+/g, " ").slice(0, 1200);
}

function hasSelectedAnswer() {
  return Boolean(document.querySelector([
    "input[type='radio']:checked",
    "input[type='checkbox']:checked",
    "[role='radio'][aria-checked='true']",
    "[role='checkbox'][aria-checked='true']",
    "[role='option'][aria-selected='true']"
  ].join(", ")));
}

function isFinalSubmitButton(element) {
  const label = [element.textContent, element.getAttribute("aria-label"), element.getAttribute("title")]
    .filter(Boolean)
    .join(" ");

  return /(submit exam|finish|complete|hoàn thành|nộp bài|submit quiz|submit test|submit all|kết thúc)/i.test(label);
}

function getQuestionSubmitButtons() {
  return getVisibleClickables().filter((element) => {
    if (element.id === SKIP_BUTTON_ID || element.id === SUBMIT_BUTTON_ID || isFinalSubmitButton(element)) {
      return false;
    }

    const label = [element.textContent, element.getAttribute("aria-label"), element.getAttribute("title")]
      .filter(Boolean)
      .join(" ")
      .trim();

    return /^submit response$/i.test(label) && !element.disabled && element.getAttribute("aria-disabled") !== "true";
  });
}

async function autoSubmitQuiz() {
  await sleep(300);

  if (!hasSelectedAnswer()) {
    showNotice("Select answers first");
    return { submitted: 0, done: true, reason: "no-selected-answer" };
  }

  const submitButtons = getQuestionSubmitButtons();

  if (submitButtons.length === 0) {
    showNotice("Question submit buttons not found");
    return { submitted: 0, done: true, reason: "no-question-submit" };
  }

  let submitted = 0;

  for (const button of submitButtons) {
    if (!document.contains(button) || button.disabled || button.getAttribute("aria-disabled") === "true") {
      continue;
    }

    button.scrollIntoView({ block: "center", inline: "nearest" });
    await sleep(300);
    button.click();
    submitted += 1;
    showNotice(`Submitted ${submitted}/${submitButtons.length} question buttons`);
    await sleep(1200);
  }

  showNotice(`Done: submitted ${submitted} question button(s). Final submit left for you.`);
  return { submitted, done: true };
}

async function waitForPageToSettle(previousUrl, previousVideo, previousSignature, timeout = 10000) {
  const startedAt = Date.now();

  while (Date.now() - startedAt < timeout) {
    await sleep(500);
    const currentVideo = findVideo();

    const currentSignature = getPageSignature();

    if (window.location.href !== previousUrl || (currentVideo && currentVideo !== previousVideo) || currentSignature !== previousSignature) {
      await sleep(2000);
      return true;
    }
  }

  return false;
}

async function skipVideoAcrossFrames() {
  try {
    const result = await browser.runtime.sendMessage({ type: "skip-active-video-only" });
    return Boolean(result?.skipped);
  } catch (error) {
    console.warn("Manual Video Controller: all-frame video skip failed", error);
    return false;
  }
}

async function waitForSkippableVideo(timeout = 8000) {
  const startedAt = Date.now();
  let latestVideo = null;

  while (Date.now() - startedAt < timeout) {
    latestVideo = findVideo();

    if (latestVideo && Number.isFinite(latestVideo.duration) && latestVideo.duration > 0) {
      return latestVideo;
    }

    await sleep(500);
  }

  return latestVideo;
}

async function skipCourseContinuously() {
  let skippedVideos = 0;
  let jumpedItems = 0;

  showNotice("Auto skip started");

  for (let step = 0; autoSkipRunning && step < 80; step += 1) {
    await sleep(2000);

    const beforeUrl = window.location.href;
    let beforeVideo = findVideo();
    const beforeSignature = getPageSignature();

    showNotice("Checking for video...");
    const skippedAcrossFrames = await skipVideoAcrossFrames();

    if (!skippedAcrossFrames) {
      beforeVideo = await waitForSkippableVideo();
    }

    const hasVideo = skippedAcrossFrames || (beforeVideo && Number.isFinite(beforeVideo.duration) && beforeVideo.duration > 0);
    const hasQuiz = !hasVideo && isActiveQuizItem();

    if (hasVideo) {
      if (!skippedAcrossFrames && beforeVideo) {
        beforeVideo.currentTime = Math.max(0, beforeVideo.duration - 0.2);
        beforeVideo.dispatchEvent(new Event("ended"));
      }

      skippedVideos += 1;
      showNotice(`Skipped ${skippedVideos} video(s), waiting...`);
      await sleep(2500);
    } else if (hasQuiz) {
      showNotice("Quiz item detected, moving next slowly");
      await sleep(1500);
    } else {
      const activeText = getActiveCourseItemText();
      showNotice(activeText ? "No video found on active item; stopped" : "No video/active item found; stopped");
      console.warn("Manual Video Controller: stopped before next", {
        url: window.location.href,
        activeText,
        videos: document.querySelectorAll("video").length,
        iframes: document.querySelectorAll("iframe").length
      });
      return { skippedVideos, jumpedItems, done: false, reason: "no-video-on-non-quiz", activeText };
    }

    if (!autoSkipRunning) {
      break;
    }

    const navigated = goToNextCourseItem();

    if (!navigated) {
      showNotice(`Done: skipped ${skippedVideos} video(s), no next item`);
      return { skippedVideos, jumpedItems, done: true };
    }

    jumpedItems += 1;
    showNotice("Waiting for next item to load...");

    const changed = await waitForPageToSettle(beforeUrl, beforeVideo, beforeSignature);

    if (!changed) {
      showNotice("Stopped: next item did not load");
      return { skippedVideos, jumpedItems, done: false, reason: "navigation-timeout" };
    }
  }

  showNotice(autoSkipRunning ? `Stopped after limit: skipped ${skippedVideos} video(s)` : "Auto skip stopped");
  return { skippedVideos, jumpedItems, done: !autoSkipRunning };
}

function showNotice(message) {
  let notice = document.getElementById(NOTICE_ID);

  if (!notice) {
    notice = document.createElement("div");
    notice.id = NOTICE_ID;
    notice.setAttribute("role", "status");
    notice.style.position = "fixed";
    notice.style.right = "16px";
    notice.style.bottom = "16px";
    notice.style.zIndex = "2147483647";
    notice.style.padding = "10px 12px";
    notice.style.borderRadius = "8px";
    notice.style.background = "rgba(20, 20, 20, 0.9)";
    notice.style.color = "#fff";
    notice.style.font = "14px/1.4 system-ui, sans-serif";
    notice.style.boxShadow = "0 8px 24px rgba(0, 0, 0, 0.25)";
    notice.style.pointerEvents = "none";
    document.documentElement.appendChild(notice);
  }

  notice.textContent = message;
  window.clearTimeout(showNotice.timeoutId);
  showNotice.timeoutId = window.setTimeout(() => notice.remove(), 1600);
}

function controlVideo(command, settings) {
  const video = findVideo();

  if (!video) {
    showNotice("No video found on this page");
    return { handled: false, reason: "no-video" };
  }

  lastActiveVideo = video;

  if (command === "toggle-play") {
    if (video.paused) {
      video.play();
      showNotice("Video playing");
    } else {
      video.pause();
      showNotice("Video paused");
    }
    return { handled: true };
  }

  if (command === "seek-backward") {
    video.currentTime = clamp(video.currentTime - settings.seekSeconds, 0, video.duration || video.currentTime);
    showNotice(`Back ${settings.seekSeconds}s`);
    return { handled: true };
  }

  if (command === "seek-forward") {
    const duration = Number.isFinite(video.duration) ? video.duration : video.currentTime + settings.seekSeconds;
    video.currentTime = clamp(video.currentTime + settings.seekSeconds, 0, duration);
    showNotice(`Forward ${settings.seekSeconds}s`);
    return { handled: true };
  }

  if (command === "skip-video") {
    if (!autoSkipRunning) {
      autoSkipRunning = true;
      skipCourseContinuously().finally(() => {
        autoSkipRunning = false;
      });
    }
    return { handled: true, running: true };
  }

  if (command === "speed-up") {
    video.playbackRate = nearestSpeed(video.playbackRate, 1, settings);
    showNotice(`Speed ${video.playbackRate}x`);
    return { handled: true };
  }

  if (command === "speed-down") {
    video.playbackRate = nearestSpeed(video.playbackRate, -1, settings);
    showNotice(`Speed ${video.playbackRate}x`);
    return { handled: true };
  }

  if (command === "reset-speed") {
    video.playbackRate = 1;
    showNotice("Speed 1x");
    return { handled: true };
  }

  return { handled: false, reason: "unknown-command" };
}

function watchVideo(video) {
  if (observedVideos.has(video)) {
    return;
  }

  observedVideos.add(video);

  video.addEventListener("play", () => {
    lastActiveVideo = video;
  });

  video.addEventListener("ended", () => {
    browser.runtime.sendMessage({ type: "video-ended" });
  });
}

function watchExistingVideos() {
  document.querySelectorAll("video").forEach(watchVideo);
}

const observer = new MutationObserver(() => {
  watchExistingVideos();
  ensureSkipButton();
  ensureSubmitButton();
});
observer.observe(document.documentElement, { childList: true, subtree: true });
watchExistingVideos();
ensureSkipButton();
ensureSubmitButton();

browser.runtime.onMessage.addListener((message) => {
  if (message.type === "video-command") {
    return controlVideo(message.command, message.settings);
  }

  if (message.type === "settings-updated") {
    showNotice(message.settings.autoNextOnEnded ? "Auto-next after ended: on" : "Auto-next after ended: off");
  }
});
