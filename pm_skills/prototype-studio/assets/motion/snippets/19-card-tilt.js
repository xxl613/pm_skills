// Track the pointer on the OUTER .t-tilt (never transforms) and write
// rotation + glare position onto the inner card. Works for mouse
// (hover) and touch / pen (tap-hold-drag) — a touch pointermove only
// fires while a finger is down, so the press naturally drives the tilt.
const tilt = document.querySelector(".t-tilt");
const card = tilt.querySelector(".t-tilt-card");
const reduce = matchMedia("(prefers-reduced-motion: reduce)");

const MAX = 14; // peak tilt in degrees at the card edges (raise for a stronger lean)

function reset() {
  tilt.classList.remove("is-hover");
  card.classList.remove("is-tilting");
  card.style.setProperty("--tilt-rx", "0deg");
  card.style.setProperty("--tilt-ry", "0deg");
}

function track(e) {
  if (reduce.matches) return;
  const r = tilt.getBoundingClientRect();
  const px = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
  const py = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height));
  tilt.classList.add("is-hover");
  card.classList.add("is-tilting");
  card.style.setProperty("--tilt-ry", ((px - 0.5) * MAX).toFixed(2) + "deg");
  card.style.setProperty("--tilt-rx", ((0.5 - py) * MAX).toFixed(2) + "deg");
  card.style.setProperty("--tilt-gx", (px * 100).toFixed(1) + "%");
  card.style.setProperty("--tilt-gy", (py * 100).toFixed(1) + "%");
}

tilt.addEventListener("pointerdown", (e) => {
  // Touch / pen: capture so the drag keeps targeting the card even if
  // the finger drifts past its edge. Pair with touch-action: none on
  // .t-tilt so the drag tilts instead of scrolling the page.
  if (e.pointerType !== "mouse") {
    try { tilt.setPointerCapture(e.pointerId); } catch (_) {}
  }
});
tilt.addEventListener("pointermove", track);
tilt.addEventListener("pointerup", reset);
tilt.addEventListener("pointercancel", reset);
tilt.addEventListener("pointerleave", (e) => {
  // Mouse: leaving the card flattens it. Touch already reset on up.
  if (e.pointerType === "mouse") reset();
});
