(function (global) {
  "use strict";
  const KEY = "prototype-studio:coherent-fixture:v1";
  const seed = [{id:"T-001",title:"检查页面与 PRD 绑定",status:"open"},{id:"T-002",title:"核对统计计算来源",status:"done"},{id:"T-003",title:"验证取消删除",status:"open"}];
  function all() {
    const raw = localStorage.getItem(KEY);
    if (!raw) { localStorage.setItem(KEY, JSON.stringify(seed)); return seed.map(row => ({...row})); }
    const rows = JSON.parse(raw);
    if (!Array.isArray(rows) || rows.some(row => !row.id || typeof row.title !== "string" || !["open","done"].includes(row.status))) throw new Error("测试记录格式不正确，请使用重置恢复合成样例。");
    return rows;
  }
  function save(rows) { localStorage.setItem(KEY, JSON.stringify(rows)); global.dispatchEvent(new Event("fixture-change")); }
  function title(value) { const text = value.trim(); if (!text || text.length > 80) throw new Error("标题需要 1–80 个字符。"); return text; }
  function stats() { const rows = all(); const done = rows.filter(row => row.status === "done").length; return {total:rows.length,open:rows.length-done,done}; }
  global.FixtureStore = {
    all, stats,
    create(value) { const rows = all(); const text = title(value); const id = global.crypto && global.crypto.randomUUID ? global.crypto.randomUUID() : "T-" + Date.now() + "-" + Math.random().toString(16).slice(2); rows.push({id,title:text,status:"open"}); save(rows); },
    update(id,value) { const text = title(value); const rows = all(); const row = rows.find(item => item.id === id); if (!row) throw new Error("记录已不存在，请刷新列表。"); row.title = text; save(rows); },
    toggle(id) { const rows = all(); const row = rows.find(item => item.id === id); if (!row) throw new Error("记录已不存在，请刷新列表。"); row.status = row.status === "done" ? "open" : "done"; save(rows); },
    remove(id) { save(all().filter(row => row.id !== id)); },
    reset() { save(seed.map(row => ({...row}))); }
  };
})(window);
