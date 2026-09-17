// Three-phase text swap:
//   1. Add .is-exit              — old text exits up with blur.
//   2. After --text-swap-dur, swap textContent and add .is-enter-start
//      (jumps to "below, no transition"), force a reflow.
//   3. Remove .is-enter-start    — new text animates back to rest.
const el = document.querySelector(".t-text-swap");
const dur = parseFloat(
  getComputedStyle(document.documentElement).getPropertyValue("--text-swap-dur")
) || 200;

function swapText(next) {
  el.classList.add("is-exit");
  setTimeout(() => {
    el.textContent = next;
    el.classList.remove("is-exit");
    el.classList.add("is-enter-start");
    void el.offsetHeight; // force reflow so the next change transitions
    el.classList.remove("is-enter-start");
  }, dur);
}
