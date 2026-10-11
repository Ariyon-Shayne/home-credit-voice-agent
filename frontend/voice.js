let RetellClientClass = null;

const $ = (selector) => document.querySelector(selector);
const config = window.RETELL_CONFIG || {};
const modal = $("#nameModal");
const nameForm = $("#nameForm");
const nameInput = $("#customerNameInput");
const startButton = $("#assistantButton");
const endButton = $("#endCallButton");
const statusBox = $("#assistantStatus");
const statusText = $("#statusText");
const hint = $("#assistantHint");
const toast = $("#toast");

let customerName = "";
let retellClient = null;
let activeCall = null;
let toastTimer = null;

function showToast(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 4500);
}

function setStatus(message, ready = false) {
  statusText.textContent = message;
  statusBox.classList.toggle("ready", ready);
}

function hasConfig() {
  const key = (config.publicKey || "").trim();
  const agent = (config.voiceAgentId || "").trim();
  return Boolean(key && agent && !key.includes("YOUR_") && !agent.includes("YOUR_"));
}

// Ask for a customer name on every fresh page load. It stays in memory only.
document.body.classList.add("modal-open");
nameForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const enteredName = nameInput.value.trim().replace(/\s+/g, " ");
  if (!enteredName) {
    nameInput.setCustomValidity("Please enter your name.");
    nameInput.reportValidity();
    return;
  }
  nameInput.setCustomValidity("");
  customerName = enteredName;
  modal.hidden = true;
  document.body.classList.remove("modal-open");
  hint.textContent = `Ready to start a voice conversation as ${customerName}.`;
  if (hasConfig()) {
    setStatus(`Ready to talk with ${customerName}`, true);
  } else {
    setStatus("Voice assistant setup needed", false);
    hint.textContent = "Name saved for this page. Add a Retell Public Key and Voice Agent ID in config.js to enable calls.";
  }
  showToast(`Welcome, ${customerName}. Your name will be passed to the voice assistant when the call starts.`);
});

nameInput.addEventListener("input", () => nameInput.setCustomValidity(""));

// Allow the user to update the name from the main call area.
const changeNameButton = $("#changeNameButton");
changeNameButton?.addEventListener("click", () => {
  if (activeCall && activeCall.status !== "ended") {
    showToast("End the current call before changing the customer name.");
    return;
  }
  nameInput.value = customerName;
  modal.hidden = false;
  document.body.classList.add("modal-open");
  nameInput.focus();
});

startButton.addEventListener("click", async () => {
  if (!customerName) {
    modal.hidden = false;
    document.body.classList.add("modal-open");
    nameInput.focus();
    return;
  }
  if (!hasConfig()) {
    showToast("Configure the Retell Public Key and Voice Agent ID in frontend/config.js first.");
    return;
  }
  if (activeCall && activeCall.status !== "ended") {
    showToast("A voice call is already in progress.");
    return;
  }

  startButton.disabled = true;
  startButton.innerHTML = 'Connecting… <span>◌</span>';
  setStatus("Connecting to the voice assistant…", false);
  hint.textContent = "Allow microphone access if your browser asks.";

  try {
    if (!RetellClientClass) {
      const sdkModule = await import("https://esm.sh/retell-client-js-sdk@latest");
      RetellClientClass = sdkModule.RetellClient;
      if (!RetellClientClass) throw new Error("Retell Web SDK did not load correctly.");
    }
    if (!retellClient) {
      retellClient = new RetellClientClass({ key: config.publicKey.trim() });
    }
    activeCall = retellClient.createWebCall({
      agent_id: config.voiceAgentId.trim(),
      retell_llm_dynamic_variables: {
        customer_name: customerName,
        company_name: "Home Credit",
        language_to_speak: "English"
      },
      hooks: {
        onStatus: (status) => {
          if (status === "live") {
            setStatus(`Connected — speaking with ${customerName}`, true);
            hint.textContent = "You can speak naturally, interrupt, or correct an answer.";
            startButton.hidden = true;
            endButton.hidden = false;
            endButton.disabled = false;
          } else if (status === "ended") {
            resetCallControls();
            setStatus("Call ended", false);
            hint.textContent = `You can start another call as ${customerName}.`;
          } else {
            setStatus("Connecting to the voice assistant…", false);
          }
        },
        onError: (error) => {
          console.error("Retell web call error:", error);
          resetCallControls();
          setStatus("Could not connect", false);
          hint.textContent = "Check microphone permission, your public key domain allowlist, and the Voice Agent ID.";
          showToast(error?.message || "The call could not start. Check the browser console and Retell configuration.");
        },
        onEnd: () => {
          resetCallControls();
          if (statusText.textContent.startsWith("Connected")) setStatus("Call ended", false);
        }
      }
    });
    endButton.hidden = false;
    endButton.disabled = false;
    await activeCall.startAudioPlayback?.().catch(() => {});
  } catch (error) {
    console.error("Could not create Retell web call:", error);
    resetCallControls();
    setStatus("Could not connect", false);
    hint.textContent = "Check your Retell configuration and browser microphone permission.";
    showToast(error?.message || "Unable to start the voice call.");
  }
});

endButton.addEventListener("click", async () => {
  endButton.disabled = true;
  endButton.textContent = "Ending call…";
  try {
    await activeCall?.end();
  } catch (error) {
    console.error("Error ending Retell call:", error);
    showToast("Could not end the call cleanly. You can close the call from the browser session.");
  } finally {
    resetCallControls();
    setStatus("Call ended", false);
    hint.textContent = customerName ? `You can start another call as ${customerName}.` : "Enter your name to begin.";
  }
});

function resetCallControls() {
  startButton.hidden = false;
  startButton.disabled = false;
  startButton.innerHTML = 'Start voice call <span>→</span>';
  endButton.hidden = true;
  endButton.disabled = false;
  endButton.innerHTML = 'End call <span>■</span>';
  activeCall = null;
}

// Keep name changes available from the assistant section without cluttering the hero.
if (changeNameButton) changeNameButton.textContent = "Change name";
