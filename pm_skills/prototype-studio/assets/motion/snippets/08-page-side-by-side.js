// Flip data-page on the container — the CSS handles the rest.
// Set --page-exit-enabled: 0 on the container if you want pages to
// fade without sliding (useful on first paint).
const slider = document.querySelector(".t-page-slide");
function showPage(n) {
  slider.setAttribute("data-page", String(n));
}
