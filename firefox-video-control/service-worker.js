const DEFAULT_SETTINGS = {
  autoNextOnEnded: false,
  seekSeconds: 10,
  minSpeed: 0.25,
  maxSpeed: 4
};

async function getSettings() {
  return browser.storage.local.get(DEFAULT_SETTINGS);
}

async function sendToActiveTab(message) {
  const tabs = await browser.tabs.query({ active: true, currentWindow: true });
  const activeTab = tabs[0];

  if (!activeTab || typeof activeTab.id !== "number") {
    return;
  }

  try {
    const response = await browser.tabs.sendMessage(activeTab.id, message);
    return { delivered: true, tabId: activeTab.id, response };
  } catch (error) {
    console.warn("Manual Video Controller: cannot reach content script", error);
    return { delivered: false, error: String(error) };
  }
}

async function goToNextCourseItem(tabId) {
  const results = await browser.scripting.executeScript({
    target: { tabId },
    func: () => {
      const isVisible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
      };

      const clickableSelector = [
        "a[href]",
        "button",
        "[role='button']",
        "[role='link']",
        "[tabindex]:not([tabindex='-1'])"
      ].join(", ");
      const clickables = Array.from(document.querySelectorAll(clickableSelector)).filter(isVisible);
      const nextTextPattern = /(next|tiếp|kế tiếp|bài tiếp|sau)/i;
      const explicitNext = clickables.find((element) => {
        const label = [
          element.textContent,
          element.getAttribute("aria-label"),
          element.getAttribute("title")
        ].filter(Boolean).join(" ");
        return nextTextPattern.test(label) && !element.disabled && element.getAttribute("aria-disabled") !== "true";
      });

      if (explicitNext) {
        explicitNext.click();
        return { navigated: true, method: "next-button" };
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
      const activeElement = document.querySelector(activeSelector);

      if (!activeElement) {
        return { navigated: false, reason: "no-active-item" };
      }

      const sidebar = activeElement.closest("aside, nav, [role='navigation'], [class*='sidebar'], [class*='sider'], [class*='menu'], [class*='lesson'], [class*='course'], [class*='playlist']") || document;
      const sidebarClickables = Array.from(sidebar.querySelectorAll(clickableSelector)).filter(isVisible);
      const activeClickable = activeElement.matches(clickableSelector) ? activeElement : activeElement.closest(clickableSelector);
      const currentIndex = sidebarClickables.findIndex((element) => element === activeClickable || element.contains(activeElement));

      if (currentIndex === -1) {
        return { navigated: false, reason: "active-item-not-clickable" };
      }

      const nextClickable = sidebarClickables.slice(currentIndex + 1).find((element) => {
        const text = element.textContent.trim();
        return text.length > 0 && !element.disabled && element.getAttribute("aria-disabled") !== "true";
      });

      if (!nextClickable) {
        return { navigated: false, reason: "no-next-item" };
      }

      nextClickable.scrollIntoView({ block: "center", inline: "nearest" });
      nextClickable.click();
      return { navigated: true, method: "sidebar-next-item" };
    }
  });

  return results[0]?.result || { navigated: false, reason: "no-result" };
}
async function skipVideoInActiveTab({ navigate = true } = {}) {
  const tabs = await browser.tabs.query({ active: true, currentWindow: true });
  const activeTab = tabs[0];

  if (!activeTab || typeof activeTab.id !== "number") {
    return { skipped: false, reason: "no-active-tab" };
  }

  try {
    const results = await browser.scripting.executeScript({
      target: { tabId: activeTab.id, allFrames: true },
      func: () => {
        const videos = Array.from(document.querySelectorAll("video"));

        if (videos.length === 0) {
          return { skipped: false, reason: "no-video" };
        }

        const video = videos.find((candidate) => !candidate.paused && !candidate.ended) || videos[0];

        if (!Number.isFinite(video.duration) || video.duration <= 0) {
          return { skipped: false, reason: "unknown-duration" };
        }

        video.currentTime = Math.max(0, video.duration - 0.2);
        video.dispatchEvent(new Event("ended"));
        return { skipped: true };
      }
    });

    const skipped = results.some((result) => result.result?.skipped);

    if (skipped) {
      if (!navigate) {
        return { skipped: true };
      }

      const navigation = await goToNextCourseItem(activeTab.id);
      return { skipped: true, navigation };
    }

    return { skipped: false, reason: "no-skippable-video" };
  } catch (error) {
    console.warn("Manual Video Controller: cannot skip active video", error);
    return { skipped: false, error: String(error) };
  }
}

browser.commands.onCommand.addListener(async (command) => {
  const settings = await getSettings();

  if (command === "toggle-auto-next") {
    const nextValue = !settings.autoNextOnEnded;
    await browser.storage.local.set({ autoNextOnEnded: nextValue });
    await sendToActiveTab({ type: "settings-updated", settings: { ...settings, autoNextOnEnded: nextValue } });
    return;
  }

  if (command === "skip-video") {
    await skipVideoInActiveTab();
    return;
  }

  await sendToActiveTab({ type: "video-command", command, settings });
});

browser.runtime.onMessage.addListener((message, sender) => {
  if (message.type === "video-ended") {
    return getSettings().then((settings) => {
      if (settings.autoNextOnEnded && sender.tab && typeof sender.tab.id === "number") {
        return goToNextCourseItem(sender.tab.id);
      }
      return undefined;
    });
  }

  if (message.type === "skip-active-video-only") {
    return skipVideoInActiveTab({ navigate: false });
  }

  if (message.type === "get-settings") {
    return getSettings();
  }

  if (message.type === "set-settings") {
    return browser.storage.local.set(message.settings).then(() => getSettings());
  }

  if (message.type === "popup-command") {
    if (message.command === "skip-video") {
      return skipVideoInActiveTab();
    }

    return getSettings().then((settings) => sendToActiveTab({
      type: "video-command",
      command: message.command,
      settings
    }));
  }

  return undefined;
});
