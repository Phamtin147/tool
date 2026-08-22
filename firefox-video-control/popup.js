/**
 * LevelUp Video Control - Popup
 * 
 * @author Amtia / Phamtin147 (https://github.com/Phamtin147)
 */

const statusEl = document.getElementById("status");
const autoNextEl = document.getElementById("auto-next");

function setStatus(message) {
  statusEl.textContent = message;
  window.clearTimeout(setStatus.timeoutId);
  setStatus.timeoutId = window.setTimeout(() => {
    statusEl.textContent = "";
  }, 1800);
}

async function loadSettings() {
  const settings = await browser.runtime.sendMessage({ type: "get-settings" });
  autoNextEl.checked = Boolean(settings.autoNextOnEnded);
}

async function sendCommand(command) {
  await browser.runtime.sendMessage({ type: "popup-command", command });
  setStatus("Đã gửi lệnh tới tab hiện tại");
}

document.querySelectorAll("button[data-command]").forEach((button) => {
  button.addEventListener("click", () => {
    sendCommand(button.dataset.command);
  });
});

autoNextEl.addEventListener("change", async () => {
  await browser.runtime.sendMessage({
    type: "set-settings",
    settings: { autoNextOnEnded: autoNextEl.checked }
  });
  setStatus(autoNextEl.checked ? "Auto-next đã bật" : "Auto-next đã tắt");
});

loadSettings().catch((error) => {
  setStatus("Không đọc được cài đặt extension");
  console.error(error);
});
