const button = document.getElementById("toggle");
const details = document.getElementById("details");
button.addEventListener("click", () => {
  const expanded = button.getAttribute("aria-expanded") === "true";
  button.setAttribute("aria-expanded", String(!expanded));
  details.hidden = expanded;
  button.textContent = expanded ? "展开说明" : "收起说明";
});
