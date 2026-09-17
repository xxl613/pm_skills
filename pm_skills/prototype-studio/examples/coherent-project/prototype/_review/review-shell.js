/* Prototype Studio review runtime. Business UI and PRD sources are never edited here. */
(function () {
  "use strict";
  if (document.getElementById("ps-review")) return;
  const script = document.currentScript;
  const rootURL = new URL("../", script.src);
  const data = window.PROTOTYPE_REVIEW_DATA;
  const host = document.createElement("div");
  host.id = "ps-review";
  const escape = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const icon = kind => kind === "nav"
    ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6h12M9 12h12M9 18h12"/><circle cx="3" cy="6" r="1"/><circle cx="3" cy="12" r="1"/><circle cx="3" cy="18" r="1"/></svg>'
    : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6M9 16h6"/></svg>';
  host.innerHTML = '<div class="ps-toolbar" aria-label="原型评审工具"><button type="button" data-open="pages" aria-label="打开页面列表" title="页面列表">' + icon("nav") + '</button><button type="button" data-open="prd" aria-label="打开当前页面 PRD" title="页面 PRD">' + icon("prd") + '</button></div><div class="ps-backdrop" hidden></div><section class="ps-panel" role="dialog" aria-modal="true" aria-labelledby="ps-panel-title" hidden tabindex="-1"><header><div><p class="ps-eyebrow">原型评审</p><h2 id="ps-panel-title"></h2></div><button type="button" class="ps-close" aria-label="关闭评审面板">×</button></header><div class="ps-body"></div></section>';
  document.documentElement.appendChild(host);
  const panel = host.querySelector(".ps-panel"), body = host.querySelector(".ps-body"), backdrop = host.querySelector(".ps-backdrop");
  let opener = null, openKind = null;
  function route(url) {
    const pairs = Array.from(url.searchParams.entries()).sort((a, b) => a[0].localeCompare(b[0]) || a[1].localeCompare(b[1]));
    let pathname, hash;
    try { pathname = decodeURIComponent(url.pathname); hash = decodeURIComponent(url.hash.slice(1)); }
    catch (_) { pathname = url.pathname; hash = url.hash.slice(1); }
    return JSON.stringify([pathname, pairs, hash]);
  }
  function activePage() {
    return data && Array.isArray(data.pages) && data.pages.find(page => route(new URL(page.path, rootURL)) === route(new URL(location.href)));
  }
  function inline(text, sourcePath) {
    let result = escape(text);
    result = result.replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    return result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, title, target) => {
      const decoded = target.replace(/&amp;/g, "&");
      let href;
      try { href = new URL(decoded, new URL(sourcePath, rootURL)); }
      catch (_) { return title + " (" + target + ")"; }
      if (!["http:", "https:", "file:"].includes(href.protocol)) return title;
      return '<a href="' + escape(href.href) + '" target="_blank" rel="noopener noreferrer">' + title + '</a>';
    });
  }
  function markdown(text, sourcePath) {
    const lines = text.replace(/\r/g, "").split("\n");
    let out = "", fence = false, code = [], list = false;
    const closeList = () => { if (list) { out += "</ul>"; list = false; } };
    const cells = row => {
      const values = [];
      let cell = "", escaped = false;
      for (const char of row.trim().slice(1)) {
        if (char === "|" && !escaped) { values.push(inline(cell.trim(), sourcePath)); cell = ""; continue; }
        if (char === "|" && escaped) cell = cell.slice(0, -1);
        cell += char;
        escaped = char === "\\" ? !escaped : false;
      }
      if (cell.trim()) values.push(inline(cell.trim(), sourcePath));
      return values;
    };
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (/^```/.test(line)) {
        closeList();
        if (fence) { out += "<pre><code>" + escape(code.join("\n")) + "</code></pre>"; code = []; }
        fence = !fence; continue;
      }
      if (fence) { code.push(line); continue; }
      if (/^\|/.test(line) && i + 1 < lines.length && /^\|[\s:|-]+\|\s*$/.test(lines[i + 1])) {
        closeList();
        out += '<div class="ps-table-wrap"><table><thead><tr>' + cells(line).map(cell => "<th>" + cell + "</th>").join("") + "</tr></thead><tbody>";
        i += 1;
        while (i + 1 < lines.length && /^\|/.test(lines[i + 1])) { i++; out += "<tr>" + cells(lines[i]).map(cell => "<td>" + cell + "</td>").join("") + "</tr>"; }
        out += "</tbody></table></div>"; continue;
      }
      const heading = line.match(/^(#{1,6})\s+(.+)$/);
      if (heading) { closeList(); const level = Math.min(heading[1].length + 1, 6); out += "<h" + level + ">" + inline(heading[2], sourcePath) + "</h" + level + ">"; }
      else if (/^\s*[-*]\s+/.test(line)) { if (!list) { out += "<ul>"; list = true; } out += "<li>" + inline(line.replace(/^\s*[-*]\s+/, ""), sourcePath) + "</li>"; }
      else { closeList(); if (line.trim()) out += "<p>" + inline(line.replace(/^>\s?/, ""), sourcePath) + "</p>"; }
    }
    closeList();
    if (fence) out += "<pre><code>" + escape(code.join("\n")) + "</code></pre>";
    return out;
  }
  function statuses(page) {
    const labels = [["implemented", "已实现", "未实现"], ["verified", "已验证", "未验证"], ["userReviewed", "用户已评审", "用户未评审"]];
    return '<div class="ps-statuses">' + labels.map(([key, yes, no]) => '<span class="ps-status ' + (page.status[key] ? "is-done" : "") + '">' + (page.status[key] ? "✓ " + yes : "○ " + no) + "</span>").join("") + "</div>";
  }
  function performanceTable(page) {
    const records = (data.decisions || []).filter(item => item.kind === "performance" && item.affectedPages.includes(page.id));
    if (!records.length) return '<section class="ps-performance"><h3>性能确认</h3><p>本页尚无性能决策记录；交付验收仍需检查是否遗漏高成本能力。</p></section>';
    return '<section class="ps-performance"><h3>性能与生成成本确认表</h3><div class="ps-table-wrap"><table><thead><tr>' + ["字段 / 决策", "触发与频率", "影响", "替代方案", "测量依据", "决定 / 用户证据"].map(s => "<th>" + s + "</th>").join("") + '</tr></thead><tbody>' + records.map(item => {
      const cost = item.performance || {};
      return '<tr>' + [((data.performanceFields || {})[item.id] || ["页面级能力"]).join(", ") + " / " + item.id,
        (cost.trigger || "待补充") + "；" + (cost.frequency || "待补充"),
        (cost.highCost ? "高成本；" : "") + (cost.impact || "待评估"), cost.alternative || "待评估", (cost.measurement || "unknown") + "；" + (cost.evidence || "尚无测量证据"),
        item.status + "；" + (item.answer || "待用户确认") + "；" + (item.evidence || "尚无用户确认")].map(s => '<td>' + escape(s) + '</td>').join("") + '</tr>';
    }).join("") + '</tbody></table></div></section>';
  }
  function render(kind) {
    const current = activePage();
    host.querySelector("#ps-panel-title").textContent = kind === "pages" ? "页面列表" : (current ? current.title + " · PRD" : "页面 PRD");
    if (!data || !Array.isArray(data.pages)) { body.innerHTML = '<p class="ps-error" role="alert">评审数据未加载。请检查 review-data.js 并重新生成；此处不生成替代 PRD。</p>'; return; }
    const fixture = data.fixtureOnly ? '<p class="ps-notice">合成测试样例 · 所有业务记录仅用于验证一致性，未经用户确认为真实业务数据。</p>' : "";
    if (kind === "pages") {
      body.innerHTML = fixture + '<p class="ps-project">' + escape(data.title) + '</p>' + (data.pages.length ? '<nav aria-label="原型页面"><ul class="ps-pages">' + data.pages.map(page => '<li><a href="' + escape(new URL(page.path, rootURL).href) + '"' + (current && current.id === page.id ? ' aria-current="page"' : "") + '><span>' + escape(page.title) + '</span><small>' + escape(page.path) + '</small></a>' + statuses(page) + '</li>').join("") + '</ul></nav>' : '<p class="ps-empty">尚未登记页面。页面创建后应同时绑定独立 PRD。</p>');
    } else if (!current) {
      body.innerHTML = fixture + '<p class="ps-error" role="alert">当前路径、查询参数或锚点未登记，无法绑定页面 PRD。请更新页面清单后重新生成。</p>';
    } else if (!current.prdMarkdown || !current.prdMarkdown.trim()) {
      body.innerHTML = fixture + '<p class="ps-error" role="alert">当前页面缺少 PRD 内容，请先补齐源文件。</p>';
    } else {
      const pending = (data.decisions || []).filter(item => item.status === "pending" && item.affectedPages.includes(current.id));
      body.innerHTML = fixture + statuses(current) + (pending.length ? '<p class="ps-notice">本页有 ' + pending.length + ' 项待确认；待确认内容不代表正式需求已通过。</p>' : "") + '<article class="ps-markdown">' + markdown(current.prdMarkdown, current.prd) + '</article>' + performanceTable(current) + '<details class="ps-source"><summary>查看完整 Markdown 源文</summary><pre></pre></details><p class="ps-source-note">来源：' + escape(current.prd) + ' · 源摘要 ' + escape(data.sourceHash.slice(0, 12)) + '。生成时间的一致性由同步检查验证，业务语义需另行验收。</p>';
      body.querySelector(".ps-source pre").textContent = current.prdMarkdown;
    }
  }
  function close() {
    panel.hidden = true; backdrop.hidden = true; openKind = null;
    if (opener) { opener.setAttribute("aria-expanded", "false"); opener.focus(); }
  }
  host.querySelectorAll("[data-open]").forEach(button => {
    button.setAttribute("aria-haspopup", "dialog"); button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", () => {
      if (openKind === button.dataset.open) { close(); return; }
      if (opener) opener.setAttribute("aria-expanded", "false");
      opener = button; openKind = button.dataset.open; render(openKind);
      panel.hidden = false; backdrop.hidden = false; button.setAttribute("aria-expanded", "true"); panel.focus();
    });
  });
  host.querySelector(".ps-close").addEventListener("click", close);
  backdrop.addEventListener("click", close);
  document.addEventListener("keydown", event => {
    if (!openKind) return;
    if (event.key === "Escape") { event.preventDefault(); close(); }
    if (event.key === "Tab") {
      const focusable = Array.from(panel.querySelectorAll('a[href],button:not([disabled]),summary,[tabindex="0"]'));
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (!first) { event.preventDefault(); panel.focus(); }
      else if (event.shiftKey && (document.activeElement === first || document.activeElement === panel)) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && (document.activeElement === last || document.activeElement === panel)) { event.preventDefault(); first.focus(); }
    }
  });
  ["popstate", "hashchange"].forEach(name => window.addEventListener(name, () => { if (openKind) render(openKind); }));
})();
