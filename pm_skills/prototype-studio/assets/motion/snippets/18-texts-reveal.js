const block = document.querySelector(".t-stagger");

function showText() {
  block.classList.remove("is-hiding");
  block.classList.remove("is-shown");
  void block.offsetHeight;
  block.classList.add("is-shown");
}
function hideText() {
  block.classList.add("is-hiding");
  block.classList.remove("is-shown");
  setTimeout(() => block.classList.remove("is-hiding"), 200);
}
