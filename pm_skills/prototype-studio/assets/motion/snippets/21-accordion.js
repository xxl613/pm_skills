// Toggle data-open on the item; CSS owns the height + chevron morph.
const acc = document.querySelector(".t-acc");
const head = acc.querySelector(".t-acc-head");

head.addEventListener("click", () => {
  const open = acc.getAttribute("data-open") === "true";
  acc.setAttribute("data-open", String(!open));
  head.setAttribute("aria-expanded", String(!open));
});
