// Distance-falloff lift with direction-aware easing. The trick
// is setting transition-timing-function inline BEFORE writing the
// CSS variables — the browser uses whatever timing-function is
// current at the moment a transitionable property changes, so this
// gives us ease-in on the way up and a bouncy spring on the return
// without two separate transition declarations.
const root = document.querySelector(".t-avatar-group");
const avatars = Array.from(root.querySelectorAll(".t-avatar"));
const cs = getComputedStyle(document.documentElement);
const num = (name, fb) => {
  const v = parseFloat(cs.getPropertyValue(name));
  return Number.isFinite(v) ? v : fb;
};
const ease = (name, fb) =>
  cs.getPropertyValue(name).trim() || fb;

function setShifts(activeIdx, phase) {
  const lift    = num("--avatar-lift", -4);
  const falloff = num("--avatar-falloff", 0.45);
  const scale   = num("--avatar-scale", 1.05);
  const tf      = phase === "out"
    ? ease("--avatar-ease-out", "cubic-bezier(0.34, 3.85, 0.64, 1)")
    : ease("--avatar-ease-in",  "cubic-bezier(0.22, 1, 0.36, 1)");

  avatars.forEach((el, i) => {
    el.style.transitionTimingFunction = tf;
    if (activeIdx == null) {
      el.style.setProperty("--shift", "0px");
      el.style.setProperty("--scale-active", "1");
      return;
    }
    const d = Math.abs(i - activeIdx);
    el.style.setProperty(
      "--shift",
      (lift * Math.pow(falloff, d)).toFixed(3) + "px"
    );
    el.style.setProperty(
      "--scale-active",
      i === activeIdx ? String(scale) : "1"
    );
  });
}

avatars.forEach((el, i) => {
  el.addEventListener("mouseenter", () => setShifts(i, "in"));
});
root.addEventListener("mouseleave", () => setShifts(null, "out"));
