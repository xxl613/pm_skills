// Replay the digit pop-in: remove .is-animating, swap the digit spans,
// force a reflow, then re-add .is-animating. Mark the last two digits
// with data-stagger="1" / "2" so they ride in 1× / 2× --digit-stagger
// behind the leading digits.
const group = document.querySelector(".t-digit-group");

function setDigits(str) {
  group.classList.remove("is-animating");
  group.replaceChildren();
  const chars = str.split("");
  chars.forEach((ch, i) => {
    const span = document.createElement("span");
    span.className = "t-digit";
    span.textContent = ch;
    if (i === chars.length - 2) span.dataset.stagger = "1";
    else if (i === chars.length - 1) span.dataset.stagger = "2";
    group.appendChild(span);
  });
  void group.offsetHeight; // force reflow
  group.classList.add("is-animating");
}
