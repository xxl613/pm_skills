const ICONS = "../icons/";
const MEDIA = "../media/";

function statusBar() {
  return `<div class="v5m-statusbar"><span>9:41</span><span class="v5m-island"></span><span class="v5m-status-icons"><span class="v5m-signal">▂▄▆█</span><span class="v5m-wifi">⌁</span><span class="v5m-battery"></span></span></div>`;
}

function iconButton(src, label) {
  return `<button class="v5m-iconbtn" aria-label="${label}"><img src="${ICONS}${src}" alt="" /></button>`;
}

function topbar({ title = "小管家", badge = "助教", simple = false } = {}) {
  if (simple) {
    return `<header class="v5m-topbar v5m-topbar--title"><button class="v5m-iconbtn v5m-back" aria-label="返回"></button><div class="v5m-topbar__center"><span class="v5m-topbar__name">${title}</span></div><span></span></header>`;
  }
  return `<header class="v5m-topbar"><button class="v5m-iconbtn v5m-back" aria-label="返回"></button><div class="v5m-topbar__center"><button class="v5m-iconbtn v5m-menu" aria-label="会话菜单"></button><span class="v5m-topbar__name">${title}</span><span class="v5m-topbar__badge">${badge}</span></div><div class="v5m-topbar__actions">${iconButton("composer-phone.svg", "通话")}${iconButton("topbar-speaker.svg", "播报")}</div></header>`;
}

function safeComposer(placeholder = "发送消息或按住说话") {
  return `<div class="v5m-composer-wrap"><div class="v5m-composer">${iconButton("composer-plus.svg", "添加")}<span class="v5m-composer__placeholder">${placeholder}</span>${iconButton("composer-mic.svg", "语音")}</div><div class="v5m-safe"></div></div>`;
}

function avatar() {
  return `${MEDIA}mobile-agent-avatar.png`;
}

function chatMessage(content) {
  return `<div class="v5m-agent-row"><img class="v5m-agent-avatar" src="${avatar()}" alt="小管家" /><div><div class="v5m-agent-name">小管家</div><div class="v5m-agent-bubble">${content}</div></div></div>`;
}

function shell(content, options = {}) {
  return `${statusBar()}${topbar(options)}${content}`;
}

function portal() {
  return `${statusBar()}<header class="v5m-topbar v5m-topbar--title"><span></span><div class="v5m-topbar__center"><span class="v5m-topbar__name">V5 助教</span></div>${iconButton("topbar-history.svg", "历史")}</header><section class="v5m-content"><div class="v5m-greeting"><p class="v5m-greeting__eyebrow"><img class="v5m-greeting__avatar" src="${avatar()}" alt="" />Hi，老师好！</p><h1>今天想先处理哪项教学工作？</h1></div><div class="v5m-hero"><img src="${MEDIA}home-agent-cast.png" alt="V5 专员团队" /><h2>让专员协作，把复杂工作做完整</h2><p>备课、作业、学情分析都可以直接说</p></div><button class="v5m-btn v5m-btn--dark v5m-btn--block">开始和小管家对话</button></section><nav class="v5m-tabbar"><span class="v5m-tab v5m-tab--active"><img src="${ICONS}nav-v5-assistant.svg" alt="" />助教</span><span class="v5m-tab"><img src="${ICONS}nav-course.svg" alt="" />课程</span><span class="v5m-tab"><img src="${ICONS}nav-resource-lib.svg" alt="" />资源</span><span class="v5m-tab"><img src="${ICONS}app-grid.svg" alt="" />我的</span></nav>`;
}

function chat() {
  const content = `<section class="v5m-content"><div class="v5m-greeting"><p class="v5m-greeting__eyebrow"><img class="v5m-greeting__avatar" src="${avatar()}" alt="" />Hi，我是小管家！</p><h1>您的专属助教，随时为您提供帮助</h1></div><div class="v5m-hero"><img src="${MEDIA}portal-hero-3.png" alt="PPT 作品预览" /><h2>PPT生成，一键搞定</h2><p>打破AI“越做越差”的上下文天花板</p><button class="v5m-pill-primary">立即尝试</button></div></section>${safeComposer()}`;
  return shell(content);
}

function composer() {
  const content = `<section class="v5m-content"><div class="v5m-date">2026年2月18日</div><div class="v5m-user-row"><div class="v5m-user-bubble">帮我分析《计算机网络》的课后作业</div></div>${chatMessage("收到，我会先核对课程和作业范围，再给出分析。")}<div class="v5m-card"><div class="v5m-card__head"><div><div class="v5m-card__label">已选择课程</div><div class="v5m-card__title">计算机网络</div></div></div><div class="v5m-card__body">2024-2025 第二学期 · 作业 3</div></div></section>${safeComposer("正在输入分析要求…")}`;
  return shell(content);
}

function task() {
  const content = `<section class="v5m-content"><div class="v5m-task-hero"><div class="v5m-task-title">小管家<span class="v5m-topbar__badge">助教</span><img class="v5m-task-avatar" src="${MEDIA}agent-portrait-a.png" alt="" /></div><div class="v5m-tiles"><div class="v5m-tile">📁<br><strong>我的空间</strong><br><small>文件暂存在这里</small></div><div class="v5m-tile">⏰<br><strong>自动任务</strong><br><small>定期执行、全自动</small></div></div></div><p class="v5m-card__label">进行中的任务</p><div class="v5m-task-row"><span class="v5m-dot"></span><span><strong>批改三年级作文</strong><br><small>正在批改 25份作业</small></span><span>•••</span></div><div class="v5m-task-row"><span class="v5m-dot v5m-dot--red"></span><span><strong>生成期中复习资料</strong><br><small style="color:#ff2626">生成失败</small></span><span>•••</span></div><div class="v5m-task-row"><span class="v5m-dot v5m-dot--orange"></span><span><strong>课前自动准备</strong><br><small>等待课程资源</small></span><span>•••</span></div><div class="v5m-sheet" style="left:224px;right:12px;bottom:70px;padding:6px 12px 12px;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.16)"><button class="v5m-btn v5m-btn--block">执行计划</button><button class="v5m-btn v5m-btn--block">暂停</button><button class="v5m-btn v5m-btn--block" style="color:#ff2626">终止</button></div></section><div class="v5m-safe" style="position:absolute;left:0;right:0;bottom:0;background:#fff"></div>`;
  return shell(content, { title: "任务" });
}

function thinking() {
  const content = `<section class="v5m-content"><div class="v5m-date">2026年2月18日</div><div class="v5m-user-row"><div class="v5m-user-bubble">帮我创建《计算机网络》的课后作业</div></div>${chatMessage(`<div class="v5m-think-card"><div class="v5m-think-card__head"><span class="v5m-spinner"></span>小管家思考中…</div><div>已经收到你的请求，让我思考一下派谁来完成任务</div><p style="margin:10px 0 0;color:#4e5969">我由教务协同专员接手，先核对课程与作业目标。</p></div>`)}</section>${safeComposer()}`;
  return shell(content);
}

function agentSkill() {
  const agents = ["教学活动管理 Agent", "高德地图 Agent", "学课管理 Agent", "教师作业 Agent", "课程资源 Agent"];
  const rows = agents.map((name, index) => `<div class="v5m-list-row"><img class="v5m-list-row__icon" src="${MEDIA}agent-portrait-${["a","b","c","d"][index % 4]}.png" alt="" /><div><div class="v5m-list-row__title">${name}</div><div class="v5m-list-row__desc">我可以为你完成教学相关任务</div></div><span>›</span></div>`).join("");
  const content = `<div class="v5m-mask"></div><section class="v5m-sheet" style="max-height:680px"><div class="v5m-sheet__head"><span class="v5m-sheet__title">@智能体</span><button class="v5m-sheet__close">×</button></div><div class="v5m-search">⌕　搜索智能体</div>${rows}</section>`;
  return shell(`<section class="v5m-content"><div class="v5m-date">2026年2月18日</div></section>${content}`);
}

function feedback() {
  const content = `<div class="v5m-mask"></div><section class="v5m-sheet" style="max-height:620px"><div class="v5m-sheet__head"><span class="v5m-sheet__title">问题反馈</span><button class="v5m-sheet__close">×</button></div><div class="v5m-feedback"><div class="v5m-segment"><button class="v5m-btn v5m-btn--dark">涉及敏感词汇</button><button class="v5m-btn">其他</button></div><textarea class="v5m-textarea" placeholder="问题描述"></textarea><button class="v5m-btn v5m-btn--dark v5m-btn--block">立即反馈</button></div></section>`;
  return shell(`<section class="v5m-content"><div class="v5m-date">2026年2月18日</div><div class="v5m-user-row"><div class="v5m-user-bubble">帮我创建一份课后作业</div></div></section>${content}`);
}

function filePage() {
  const content = `<section class="v5m-content"><div class="v5m-date">2026年2月18日</div><div class="v5m-user-row"><div class="v5m-user-bubble">帮我创建《计算机网络》的课后作业</div></div>${chatMessage(`好的，我为您打开创建作业表单，您可以在右侧填写作业详情：<div class="v5m-file-card"><img src="${ICONS}file-upload.svg" onerror="this.src='${ICONS}nav-knowledge.svg'" alt="" /><div><div class="v5m-file-card__name">知识图谱与大模型幻觉</div><div class="v5m-file-card__meta">更新时间：2025-01-29</div></div></div>`)}</section>${safeComposer()}`;
  return shell(content);
}

function followup() {
  const options = ["A 自由创作", "B 提供素材", "C 自由创作", "D 我正在说话 ✓"];
  const content = `<section class="v5m-content"><div class="v5m-question"><div class="v5m-card__label">单选</div><div class="v5m-card__title">这次宣传文稿的内容来源是什么？</div>${options.map((o,i)=>`<div class="v5m-question__option ${i===3?'v5m-question__option--selected':''}">${o}</div>`).join("")}<div class="v5m-card__actions"><button class="v5m-btn">拒绝</button><button class="v5m-btn v5m-btn--dark">确认</button></div></div><div class="v5m-keyboard">${"QWERTYUIOPASDFGHJKLZXCVBNM".split("").map(k=>`<span class="v5m-key">${k}</span>`).join("")}</div></section>`;
  return shell(content);
}

function history() {
  const items = ["人生意义探讨", "植物剪树后是否可以再生", "人生意义探讨", "植物剪树后是否可以再生", "人生意义探讨", "植物剪树后是否可以再生"];
  const content = `<section class="v5m-content v5m-content--list"><div class="v5m-search">⌕　搜索</div>${items.map((title,i)=>`<article class="v5m-history-row"><div class="v5m-history-row__title">${title}<span style="float:right;color:#86909c;font-size:11px">星期一</span></div><div class="v5m-history-row__preview">感觉你对具体细节和计算机都很感兴趣，那是之后还想聊这些或者有关他人的问题，随时找我…</div></article>`).join("")}</section><div class="v5m-safe" style="position:absolute;left:0;right:0;bottom:0;background:#fff"></div>`;
  return shell(content, { title: "历史记录", simple: true });
}

function sheetAdd() {
  const sources = [["nav-knowledge.svg","相机"],["nav-resource-lib.svg","相册"],["file-upload.svg","手机文件"]];
  const content = `<section class="v5m-content"><div class="v5m-greeting"><p class="v5m-greeting__eyebrow"><img class="v5m-greeting__avatar" src="${avatar()}" alt="" />Hi，我是小管家！</p><h1>您的专属助教，随时为您提供帮助</h1></div></section><div class="v5m-mask"></div><section class="v5m-sheet"><div class="v5m-sheet__handle"></div><div class="v5m-source-grid">${sources.map(([icon,name])=>`<div class="v5m-source"><img src="${ICONS}${icon}" onerror="this.src='${ICONS}app-grid.svg'" alt="" />${name}</div>`).join("")}</div>${["课程资源库","个人资源库","工作空间","公式编辑器"].map(name=>`<div class="v5m-list-row"><img class="v5m-list-row__icon" src="${ICONS}nav-resource-lib.svg" alt="" /><div><div class="v5m-list-row__title">${name}</div><div class="v5m-list-row__desc">这里是${name}文件</div></div><span>›</span></div>`).join("")}</section>`;
  return shell(content);
}

const views = { portal, chat, composer, task, thinking, "agent-skill": agentSkill, feedback, file: filePage, followup, history, "sheet-add": sheetAdd };
const root = document.querySelector(".v5m-screen");
if (root) {
  root.innerHTML = (views[root.dataset.view] || chat)();
  if (root.dataset.view === "chat") {
    const hero = root.querySelector(".v5m-hero img");
    if (hero) hero.src = `${MEDIA}mobile-portfolio.png`;
  }
  const addButton = root.querySelector('[aria-label="添加"]');
  if (addButton) addButton.addEventListener("click", () => { location.href = "mobile-sheet-add.html"; });
  const menuButton = root.querySelector('[aria-label="会话菜单"]');
  if (menuButton) menuButton.addEventListener("click", () => { location.href = "mobile-history.html"; });
  const closeButton = root.querySelector(".v5m-sheet__close");
  if (closeButton) closeButton.addEventListener("click", () => history.back());
  const startButton = [...root.querySelectorAll("button")].find((button) => button.textContent.includes("开始和小管家对话"));
  if (startButton) startButton.addEventListener("click", () => { location.href = "mobile-chat.html"; });
  const submitButton = [...root.querySelectorAll("button")].find((button) => button.textContent.includes("立即反馈"));
  if (submitButton) submitButton.addEventListener("click", () => { submitButton.textContent = "已提交"; submitButton.disabled = true; });
  const confirmButton = [...root.querySelectorAll("button")].find((button) => button.textContent.trim() === "确认");
  if (confirmButton) confirmButton.addEventListener("click", () => { confirmButton.textContent = "已确认"; confirmButton.disabled = true; });
}
