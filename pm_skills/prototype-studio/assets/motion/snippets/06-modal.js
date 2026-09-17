// Same close-then-cleanup pattern as the dropdown — modals scale from
// --modal-scale up to 1, then on close dip to --modal-scale-close.
const modal = document.querySelector(".t-modal");
const closeMs = parseFloat(
  getComputedStyle(document.documentElement).getPropertyValue("--modal-close-dur")
) || 150;

function openModal() {
  modal.classList.remove("is-closing");
  modal.classList.add("is-open");
}
function closeModal() {
  modal.classList.remove("is-open");
  modal.classList.add("is-closing");
  setTimeout(() => modal.classList.remove("is-closing"), closeMs);
}
