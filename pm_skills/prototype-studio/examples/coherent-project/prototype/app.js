(function () {
  "use strict";
  const store = window.FixtureStore;
  const list = document.querySelector("#record-list");
  const feedback = document.querySelector("#feedback");
  const isSummary = document.body.dataset.page === "summary";
  const activeOnly = isSummary && new URLSearchParams(location.search).get("view") === "active";
  let editingId = null, deletingId = null;
  const editDialog = document.querySelector("#edit-dialog"), deleteDialog = document.querySelector("#delete-dialog");
  function message(text, error = false) { feedback.textContent = text; feedback.classList.toggle("error", error); }
  function button(label, handler, style = "") { const node = document.createElement("button"); node.type = "button"; node.textContent = label; node.className = style; node.addEventListener("click", handler); return node; }
  function render() {
    try {
      const rows = store.all(), totals = store.stats();
      document.querySelectorAll("[data-stat]").forEach(node => { node.textContent = totals[node.dataset.stat]; });
      list.replaceChildren();
      const visible = activeOnly ? rows.filter(row => row.status === "open") : rows;
      document.querySelector("#visible-count").textContent = visible.length;
      if (!visible.length) { const empty = document.createElement("p"); empty.className = "empty"; empty.textContent = activeOnly ? "没有未完成记录。" : "还没有记录，可以添加第一条。"; list.appendChild(empty); }
      visible.forEach(row => {
        const item = document.createElement("li"); item.className = "record"; item.dataset.recordId = row.id;
        const content = document.createElement("div");
        const title = document.createElement("h3"); title.textContent = row.title;
        const state = document.createElement("span"); state.className = "state " + row.status; state.textContent = row.status === "done" ? "✓ 已完成" : "○ 未完成";
        content.append(title, state); item.appendChild(content);
        if (!isSummary) {
          const actions = document.createElement("div"); actions.className = "actions";
          actions.append(button("编辑", () => { editingId = row.id; document.querySelector("#edit-title").value = row.title; editDialog.showModal(); document.querySelector("#edit-title").focus(); }),
            button(row.status === "done" ? "标为未完成" : "标为完成", () => { store.toggle(row.id); message("状态已更新，统计已同步。"); }),
            button("删除", () => { deletingId = row.id; document.querySelector("#delete-title").textContent = row.title; deleteDialog.showModal(); }, "danger"));
          item.appendChild(actions);
        }
        list.appendChild(item);
      });
    } catch (error) { message(error.message, true); }
  }
  if (activeOnly) { document.querySelector("#page-title").textContent = "仅未完成记录"; document.querySelector("#list-title").firstChild.textContent = "未完成记录 "; document.querySelectorAll("nav a").forEach(link => { if (link.getAttribute("href").includes("?view=active")) link.setAttribute("aria-current", "page"); else link.removeAttribute("aria-current"); }); }
  const form = document.querySelector("#create-form");
  if (form) form.addEventListener("submit", event => { event.preventDefault(); try { store.create(document.querySelector("#new-title").value); form.reset(); message("记录已添加。"); } catch (error) { message(error.message, true); } });
  if (editDialog) {
    document.querySelector("#edit-form").addEventListener("submit", event => { event.preventDefault(); try { store.update(editingId, document.querySelector("#edit-title").value); editDialog.close(); message("标题已保存，其他页面使用同一记录。"); } catch (error) { document.querySelector("#edit-error").textContent = error.message; } });
    document.querySelector("#edit-cancel").addEventListener("click", () => editDialog.close());
    editDialog.addEventListener("close", () => { document.querySelector("#edit-error").textContent = ""; editingId = null; });
    document.querySelector("#delete-cancel").addEventListener("click", () => deleteDialog.close());
    document.querySelector("#delete-confirm").addEventListener("click", () => { store.remove(deletingId); deleteDialog.close(); message("记录已删除，统计已同步。"); });
    deleteDialog.addEventListener("close", () => { deletingId = null; });
  }
  document.querySelector("#reset").addEventListener("click", () => { store.reset(); message("已恢复三条合成测试记录。"); });
  window.addEventListener("fixture-change", render);
  window.addEventListener("storage", render);
  window.addEventListener("pageshow", render);
  render();
})();
