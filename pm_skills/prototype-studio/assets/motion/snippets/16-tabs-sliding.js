const bar = document.querySelector(".t-tabs");
const pill = bar.querySelector(".t-tabs-pill");
const tabs = [...bar.querySelectorAll(".t-tab")];

function moveTo(tab, animate) {
  if (!animate) {
    const prev = pill.style.transition;
    pill.style.transition = "none";
    pill.style.transform = `translateX(${tab.offsetLeft}px)`;
    pill.style.width = `${tab.offsetWidth}px`;
    void pill.offsetWidth;
    pill.style.transition = prev;
  } else {
    pill.style.transform = `translateX(${tab.offsetLeft}px)`;
    pill.style.width = `${tab.offsetWidth}px`;
  }
}
const active = () =>
  tabs.find((t) => t.getAttribute("aria-selected") === "true") || tabs[0];

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) =>
      t.setAttribute("aria-selected", t === tab ? "true" : "false")
    );
    moveTo(tab, true);
  });
});
requestAnimationFrame(() => moveTo(active(), false));
window.addEventListener("resize", () => moveTo(active(), false));
