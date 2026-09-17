const skel = document.querySelector(".t-skel");
const skeleton = skel.querySelector(".t-skel-skeleton");
const cs = getComputedStyle(document.documentElement);
const num = (name, fb) => {
  const v = parseFloat(cs.getPropertyValue(name));
  return Number.isFinite(v) ? v : fb;
};

// Call when async data arrives:
function reveal() {
  skel.classList.add("is-revealed");
}

// Demo replay: snap back, pulse, then reveal.
function replay() {
  skel.classList.add("is-resetting");
  skel.classList.remove("is-revealed");
  skeleton.classList.remove("is-pulsing");
  void skeleton.offsetWidth;
  skel.classList.remove("is-resetting");
  skeleton.classList.add("is-pulsing");
  const total = num("--pulse-dur", 1000) * num("--pulse-count", 1);
  setTimeout(() => skel.classList.add("is-revealed"), total);
}
