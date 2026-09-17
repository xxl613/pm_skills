// Toggle .is-open / .is-closing with a setTimeout cleanup so the closing
// scale animates before the element resets to its pre-open rest state.
const dropdown = document.querySelector(".t-dropdown");
const closeMs = parseFloat(
  getComputedStyle(document.documentElement).getPropertyValue("--dropdown-close-dur")
) || 150;

function openDropdown() {
  dropdown.classList.remove("is-closing");
  dropdown.classList.add("is-open");
}
function closeDropdown() {
  dropdown.classList.remove("is-open");
  dropdown.classList.add("is-closing");
  setTimeout(() => dropdown.classList.remove("is-closing"), closeMs);
}
