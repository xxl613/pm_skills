// Trigger the error state, replay the shake, and schedule the
// auto-revert. Cancel any in-flight revert so the timer always
// tracks the latest call.
const wrap = document.querySelector(".t-input-wrap");
const input = wrap.querySelector(".t-input");

const cs = getComputedStyle(document.documentElement);
const ms = (name, fb) => {
  const v = parseFloat(cs.getPropertyValue(name));
  return Number.isFinite(v) ? v : fb;
};

function showError() {
  wrap.classList.add("is-error");
  input.classList.add("is-error");

  // Replay the shake from a clean baseline.
  input.classList.remove("is-shaking");
  void input.offsetWidth; // force reflow
  input.classList.add("is-shaking");

  const shakeMs =
    ms("--shake-dur-a", 80) * 2 +
    ms("--shake-dur-b", 60) * 2;
  setTimeout(() => input.classList.remove("is-shaking"), shakeMs + 20);

  // Auto-revert: hold long enough to read the message, then fade
  // border + message back to neutral via the CSS transitions.
  if (wrap._revertTimer) clearTimeout(wrap._revertTimer);
  const hold = ms("--revert-hold", 3000);
  wrap._revertTimer = setTimeout(() => {
    wrap._revertTimer = null;
    wrap.classList.remove("is-error");
    input.classList.remove("is-error");
  }, shakeMs + hold);
}

// Optional but recommended: typing cancels the auto-revert and
// clears the error so the user isn't shaking at a value they're
// already correcting.
const inputEl = wrap.querySelector("input, textarea");
  inputEl?.addEventListener("input", () => {
  if (wrap._revertTimer) {
    clearTimeout(wrap._revertTimer);
    wrap._revertTimer = null;
  }
  wrap.classList.remove("is-error");
  input.classList.remove("is-error");
});
