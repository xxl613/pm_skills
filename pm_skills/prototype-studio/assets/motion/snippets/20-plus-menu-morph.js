// Toggle data-open on the container; CSS owns the morph. Mirror the
// state to aria-expanded and close on outside click / Escape.
const morph = document.querySelector(".t-morph");
const plus = morph.querySelector(".t-morph-plus");

function setOpen(open) {
  morph.setAttribute("data-open", String(open));
  plus.setAttribute("aria-expanded", String(open));
}

plus.addEventListener("click", (e) => {
  e.stopPropagation();
  setOpen(morph.getAttribute("data-open") !== "true");
});
document.addEventListener("click", (e) => {
  if (!morph.contains(e.target)) setOpen(false);
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") setOpen(false);
});
