document.addEventListener('DOMContentLoaded', async () => {
  const apiKeyInput = document.getElementById('apiKey');
  const modelSelect = document.getElementById('modelSelect');
  const modeSelect = document.getElementById('modeSelect');
  const humanDelayInput = document.getElementById('humanDelay');
  const saveBtn = document.getElementById('saveBtn');
  const statusMsg = document.getElementById('statusMsg');

  // Load saved settings
  const storage = await chrome.storage.local.get([
    'geminiApiKey',
    'geminiModel',
    'solvingMode',
    'humanDelay'
  ]);

  if (storage.geminiApiKey) apiKeyInput.value = storage.geminiApiKey;
  if (storage.geminiModel) modelSelect.value = storage.geminiModel;
  if (storage.solvingMode) modeSelect.value = storage.solvingMode;
  if (storage.humanDelay) humanDelayInput.value = storage.humanDelay;

  saveBtn.addEventListener('click', async () => {
    const geminiApiKey = apiKeyInput.value.trim();
    const geminiModel = modelSelect.value;
    const solvingMode = modeSelect.value;
    const humanDelay = parseFloat(humanDelayInput.value) || 2.0;

    await chrome.storage.local.set({
      geminiApiKey,
      geminiModel,
      solvingMode,
      humanDelay
    });

    statusMsg.className = 'status-msg success';
    statusMsg.textContent = '✓ Đã lưu cấu hình thành công!';
    setTimeout(() => {
      statusMsg.textContent = '';
    }, 2500);
  });
});
