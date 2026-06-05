"use strict";

// ── State ──
let currentProjectId = "";
let currentSessionId = "";
let selected = new Set();
let autoRefresh = true;
let stopped = false;
let showArchived = false;
let refreshTimer = null;

// ── Data caches ──
let projectsCache = [];
let sessionsCache = [];
let sessionDetailCache = null;
let statusCache = { collector: "unknown", prompt_logging: true, last_update: "" };

// ── Formatters ──
const nf = new Intl.NumberFormat("ru-RU");
const money = n => "$" + Number(n || 0).toFixed(5);
const pct = n => (Number(n || 0) * 100).toFixed(1) + "%";

// ── API helpers ──
async function api(path) {
  try {
    const res = await fetch(path);
    if (!res.ok) return null;
    return res.json();
  } catch (e) {
    return null;
  }
}

async function apiPost(path, body) {
  try {
    const res = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) return null;
    return res.json();
  } catch (e) {
    return null;
  }
}

// ── Data loading ──
async function loadProjects() {
  const data = await api("/api/projects");
  if (data && data.projects) {
    projectsCache = data.projects;
    if (!currentProjectId && data.default_project_id) {
      currentProjectId = data.default_project_id;
    }
    if (!currentProjectId && projectsCache.length > 0) {
      currentProjectId = projectsCache[0].id;
    }
  }
  if (projectsCache.length > 0 && !currentProjectId) {
    currentProjectId = projectsCache[0].id;
  }
}

function currentProject() {
  return projectsCache.find(p => p.id === currentProjectId) || projectsCache[0] || null;
}

async function loadSessions() {
  if (!currentProjectId) { sessionsCache = []; return; }
  const data = await api("/api/sessions?project_id=" + encodeURIComponent(currentProjectId) +
    "&show_archived=" + (showArchived ? "1" : "0"));
  if (data && data.sessions) {
    sessionsCache = data.sessions;
  } else {
    sessionsCache = [];
  }
  if (sessionsCache.length > 0 && !currentSessionId) {
    currentSessionId = sessionsCache[0].id;
  }
  if (!sessionsCache.find(s => s.id === currentSessionId)) {
    currentSessionId = sessionsCache[0] ? sessionsCache[0].id : "";
  }
}

async function loadSessionDetail() {
  if (!currentProjectId || !currentSessionId) { sessionDetailCache = null; return; }
  const data = await api("/api/session?project_id=" + encodeURIComponent(currentProjectId) +
    "&session_id=" + encodeURIComponent(currentSessionId));
  sessionDetailCache = data;
}

async function loadStatus() {
  const data = await api("/api/status");
  if (data) {
    statusCache.collector = data.collector || "unknown";
    statusCache.prompt_logging = data.prompt_logging !== false;
    statusCache.last_update = data.last_update || "";
  }
}

async function refreshAll() {
  await loadProjects();
  await loadSessions();
  await loadSessionDetail();
  await loadStatus();
  populateModelFilter();
  renderAll();
}

async function refreshData() {
  await apiPost("/api/refresh", { project_id: currentProjectId, session_id: currentSessionId });
  document.getElementById("lastUpdate").textContent = new Date().toLocaleTimeString("ru-RU");
  showToast("Данные обновлены");
  await refreshAll();
}

// ── Archive ──
async function toggleArchive(sessionId) {
  const detail = await api("/api/session?project_id=" + encodeURIComponent(currentProjectId) +
    "&session_id=" + encodeURIComponent(sessionId));
  const isArchivedNow = detail && detail.archived;
  await apiPost(isArchivedNow ? "/api/unarchive" : "/api/archive", {
    project_id: currentProjectId,
    session_id: sessionId,
  });
  await loadSessions();
  renderAll();
}

function toggleArchivedVisibility() {
  showArchived = !showArchived;
  localStorage.setItem("ctm_show_archived", showArchived ? "1" : "0");
  refreshAll();
}

// ── Shutdown ──
function openShutdown() { document.getElementById("shutdownModal").style.display = "flex"; }
function closeShutdown() { document.getElementById("shutdownModal").style.display = "none"; }
async function confirmShutdown() {
  stopped = true;
  autoRefresh = false;
  if (refreshTimer) clearInterval(refreshTimer);
  closeShutdown();
  await apiPost("/api/shutdown", {});
  renderStatus();
  showToast("Монитор остановлен");
}

// ── Session helpers ──
function filteredSessions() {
  const q = (document.getElementById("q")?.value || "").toLowerCase();
  const mf = (document.getElementById("modelFilter")?.value || "");
  const rf = (document.getElementById("riskFilter")?.value || "");
  return sessionsCache.filter(s => {
    const txt = (s.title + " " + s.id + " " + s.model + " " + s.reasoning + " " + s.workdir).toLowerCase();
    const hasWarn = s.warnings_count > 0;
    return txt.includes(q) &&
      (!mf || s.model === mf) &&
      (!rf || (rf === "warnings" ? hasWarn : !hasWarn));
  });
}

function currentSession() {
  return filteredSessions().find(s => s.id === currentSessionId) || filteredSessions()[0] || null;
}

function totals(steps) {
  return steps.reduce((a, t) => {
    a.input += t.usage.input_tokens;
    a.cached += t.usage.cached_tokens;
    a.non += t.usage.non_cached_input_tokens;
    a.output += t.usage.output_tokens;
    a.reasoning += t.usage.reasoning_tokens;
    a.tool += t.usage.tool_tokens;
    a.cost += t.usage.estimated_total_cost_usd || 0;
    a.warnings += (t.warnings || []).length;
    return a;
  }, { input: 0, cached: 0, non: 0, output: 0, reasoning: 0, tool: 0, cost: 0, warnings: 0 });
}

// ── Render: left panel ──
function initProjects() {
  const sel = document.getElementById("projectSelect");
  sel.innerHTML = projectsCache.map(p => `<option value="${p.id}">${p.name}</option>`).join("");
  sel.value = currentProjectId;
}

function renderProjectInfo() {
  const p = currentProject();
  document.getElementById("projectPath").textContent = p ? p.path : "";
}

function renderSessions() {
  const list = filteredSessions();
  const root = document.getElementById("sessions");
  document.getElementById("sessionCount").textContent = `${list.length}/${sessionsCache.length}`;
  document.getElementById("archivedToggleBtn").style.borderColor = showArchived ? "rgba(124,156,255,.75)" : "";
  root.innerHTML = "";

  if (!list.length) {
    root.innerHTML = `<div class="empty small">Нет подходящих сессий</div>`;
    return;
  }

  if (!list.find(s => s.id === currentSessionId)) currentSessionId = list[0].id;

  list.forEach(s => {
    const cost = s.total_cost_usd || 0;
    const cached = (sessionsCache.find(x => x.id === s.id) || s);
    const archived = false;
    const el = document.createElement("div");
    el.className = "session" + (s.id === currentSessionId ? " active" : "");
    el.onclick = async () => {
      currentSessionId = s.id;
      selected.clear();
      await loadSessionDetail();
      renderAll();
    };
    el.innerHTML = `
      <div class="session-head">
        <div>
          <div class="session-title">${escapeHtml(s.title)}</div>
          <div class="session-id muted xsmall mono">${escapeHtml(s.id)}</div>
        </div>
        <div class="row-actions">
          <button class="icon ghost" title="Архивировать/Вернуть" onclick="event.stopPropagation();toggleArchive('${s.id}')">🗄</button>
          <span class="pill blue">${s.step_count}</span>
        </div>
      </div>
      <div class="pills">
        <span class="pill">${escapeHtml(s.model)}</span>
        <span class="pill purple">${escapeHtml(s.reasoning)}</span>
        <span class="pill ${s.warnings_count ? 'yellow' : 'green'}">${s.warnings_count} warn</span>
        ${s.has_normalized ? '<span class="pill green">normalized</span>' : '<span class="pill">parsed only</span>'}
      </div>
      <div class="compact-metrics">
        <div class="cmini"><span>Cost</span><b>${money(cost)}</b></div>
        <div class="cmini"><span>Steps</span><b>${nf.format(s.step_count)}</b></div>
        <div class="cmini"><span>Model</span><b>${escapeHtml(s.model)}</b></div>
      </div>`;
    root.appendChild(el);
  });
}

// ── Render: header ──
function stat(label, value, cls) {
  return `<div class="stat ${cls || ""}"><label>${label}</label><b>${value}</b></div>`;
}

function renderHeader() {
  const s = sessionDetailCache;
  if (!s || !s.steps) {
    document.getElementById("title").textContent = "Выберите сессию";
    document.getElementById("meta").textContent = "";
    document.getElementById("stats").innerHTML = "";
    return;
  }
  const z = totals(s.steps);
  const ratio = z.input ? z.cached / z.input : 0;
  const p = currentProject();
  document.getElementById("title").textContent = s.title;
  document.getElementById("meta").textContent = `${p ? p.name : ""} · ${s.id} · ${s.date} · ${s.workdir}`;
  document.getElementById("stats").innerHTML = [
    stat("Cost", money(z.cost), "good"),
    stat("Input", nf.format(z.input), "blue"),
    stat("Cached", nf.format(z.cached), "good"),
    stat("Non-cached", nf.format(z.non), "warn"),
    stat("Cache", pct(ratio), "blue"),
    stat("Output", nf.format(z.output)),
  ].join("");
}

// ── Render: steps ──
function metric(label, value) { return `<div class="metric"><span>${label}</span><b>${value}</b></div>`; }
function kv(k, v) { return `<div class="kv"><span class="muted">${k}</span><span class="mono">${String(v)}</span></div>`; }
function escapeHtml(t) { return String(t || "").replace(/[&<>"']/g, m => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;" }[m])); }
function ellipsis(text, n) {
  text = String(text || "");
  return text.length > n ? text.slice(0, n - 1) + "\u2026" : text;
}
function textBlock(title, kind, available, text, stepIndex) {
  return `<div class="text-block" id="${kind}-${stepIndex}">
    <div class="text-head" onclick="toggleText('${kind}-${stepIndex}')">
      <div><b>${title}</b> <span class="muted xsmall">${available ? 'hidden by default' : 'not available'}</span></div>
      <button class="ghost" onclick="event.stopPropagation();toggleText('${kind}-${stepIndex}')">${available ? 'Показать' : '—'}</button>
    </div>
    <div class="text-body">${available ? escapeHtml(text) : "Текст отсутствует в telemetry/log source."}</div>
  </div>`;
}

function renderSteps() {
  const root = document.getElementById("steps");
  root.innerHTML = "";
  const s = sessionDetailCache;
  if (!s || !s.steps || !s.steps.length) {
    root.innerHTML = `<div class="loading">Нет данных по шагам</div>`;
    return;
  }
  s.steps.forEach(t => {
    const el = document.createElement("div");
    const idx = t.step_index;
    el.className = "step" + (selected.has(idx) ? " selected" : "");
    el.id = "step-" + idx;
    const u = t.usage || {};
    const env = t.environment || {};
    el.innerHTML = `
      <div class="step-head" onclick="toggleDetails(${idx})">
        <input type="checkbox" ${selected.has(idx) ? "checked" : ""} onclick="event.stopPropagation()" onchange="toggleSelect(${idx})">
        <div>
          <div class="step-title">
            <b>Step ${idx}</b>
            <span class="pill blue">${escapeHtml(t.model)}</span>
            <span class="pill purple">${escapeHtml(t.reasoning_effort)}</span>
            <span class="pill ${(t.warnings || []).length ? 'yellow' : 'green'}">${(t.warnings || []).length} warn</span>
          </div>
          <div class="metrics">
            ${metric("Cost", money(u.estimated_total_cost_usd))}
            ${metric("Input", nf.format(u.input_tokens))}
            ${metric("Cached", nf.format(u.cached_tokens))}
            ${metric("Non-cached", nf.format(u.non_cached_input_tokens))}
            ${metric("Cache", pct(u.cached_ratio))}
            ${metric("Output", nf.format(u.output_tokens))}
            ${metric("Reasoning", nf.format(u.reasoning_tokens))}
            ${metric("MCP", nf.format(env.observed_mcp_server_count))}
          </div>
          <div class="preview-row">
            <div class="preview">
              <span class="label">Prompt</span>
              <div class="text">${t.user_prompt.available ? escapeHtml(ellipsis(t.user_prompt.text, 90)) : "—"}</div>
            </div>
            <div class="preview">
              <span class="label">Answer</span>
              <div class="text">${t.assistant_answer.available ? escapeHtml(ellipsis(t.assistant_answer.text, 90)) : "—"}</div>
            </div>
          </div>
        </div>
        <div class="row-actions">
          <button class="icon" onclick="event.stopPropagation();copyStepSummary(${idx})">Copy</button>
        </div>
      </div>
      <div class="detail">
        ${textBlock("User prompt", "prompt", t.user_prompt.available, t.user_prompt.text, idx)}
        ${textBlock("Assistant answer", "answer", t.assistant_answer.available, t.assistant_answer.text, idx)}
        <div class="detail-grid">
          <div class="box">
            <h3>Tokens</h3>
            ${kv("input_tokens", u.input_tokens)}
            ${kv("cached_tokens", u.cached_tokens)}
            ${kv("non_cached", u.non_cached_input_tokens)}
            ${kv("cached_ratio", pct(u.cached_ratio))}
            ${kv("output_tokens", u.output_tokens)}
            ${kv("reasoning_tokens", u.reasoning_tokens)}
            ${kv("tool_tokens", u.tool_tokens)}
          </div>
          <div class="box">
            <h3>Cost</h3>
            ${kv("input_cost", money(u.estimated_input_cost_usd))}
            ${kv("cached_cost", money(u.estimated_cached_input_cost_usd))}
            ${kv("output_cost", money(u.estimated_output_cost_usd))}
            ${kv("total_cost", money(u.estimated_total_cost_usd))}
            ${kv("pricing", "config/token_pricing.json")}
          </div>
          <div class="box">
            <h3>Environment</h3>
            ${kv("thread_id", env.thread_id)}
            ${kv("turn_id", t.turn_id)}
            ${kv("MCP servers", (env.observed_mcp_servers || []).join(", ") || "none")}
            ${kv("plugins_count", env.enabled_plugins_count)}
            ${kv("skills_count", env.enabled_skills_count)}
            ${kv("repo_context", env.repo_context_status)}
            ${kv("warnings", (t.warnings || []).join(", ") || "none")}
          </div>
        </div>
      </div>`;
    root.appendChild(el);
  });
}

function selectedSteps() {
  if (!sessionDetailCache || !sessionDetailCache.steps) return [];
  return sessionDetailCache.steps.filter(t => selected.has(t.step_index));
}

function renderSelection() {
  const z = totals(selectedSteps());
  const ratio = z.input ? z.cached / z.input : 0;
  document.getElementById("selCount").textContent = `Selected: ${selectedSteps().length}`;
  document.getElementById("selCost").textContent = money(z.cost);
  document.getElementById("selNon").textContent = `Non-cached: ${nf.format(z.non)}`;
  document.getElementById("selCache").textContent = `Cache: ${pct(ratio)}`;
}

function renderStatus() {
  const collectorLabel = statusCache.collector || "unknown";
  const collectorDot = collectorLabel === "running" ? "" : (collectorLabel === "stopped" ? "red" : "warn");
  document.getElementById("collectorStatus").innerHTML = `<i class="dot ${collectorDot}"></i>${collectorLabel}`;

  const plEl = document.getElementById("promptLoggingStatus");
  if (plEl) {
    const plOn = statusCache.prompt_logging !== false;
    plEl.innerHTML = `<i class="dot ${plOn ? '' : 'warn'}"></i>${plOn ? 'ON' : 'OFF'}`;
  }

  document.getElementById("lastUpdate").textContent = statusCache.last_update
    ? new Date(statusCache.last_update).toLocaleTimeString("ru-RU")
    : "\u2014";
  document.getElementById("autoStatus").innerHTML = `<i class="dot ${autoRefresh && !stopped ? '' : 'warn'}"></i>${autoRefresh && !stopped ? 'ON \u00B7 3s' : 'OFF'}`;
  document.getElementById("autoBtn").textContent = "Auto: " + (autoRefresh ? "ON" : "OFF");
}

function populateModelFilter() {
  const seen = new Set();
  seen.add("mixed");
  sessionsCache.forEach(s => {
    if (s.model && s.model !== "unknown") seen.add(s.model);
  });
  const sel = document.getElementById("modelFilter");
  const currentValue = sel.value;
  sel.innerHTML = `<option value="">Все модели</option>`;
  [...seen].sort().forEach(m => {
    sel.innerHTML += `<option value="${m}">${m}</option>`;
  });
  sel.value = currentValue || "";
}

function renderAll() {
  renderProjectInfo();
  renderSessions();
  renderHeader();
  renderSteps();
  renderSelection();
  renderStatus();
}

// ── Interactions ──
function toggleDetails(i) {
  const el = document.getElementById("step-" + i);
  if (el) el.classList.toggle("open");
}

function toggleText(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle("open");
}

function toggleSelect(i) {
  selected.has(i) ? selected.delete(i) : selected.add(i);
  renderSteps();
  renderSelection();
}

function selectAll() {
  if (!sessionDetailCache || !sessionDetailCache.steps) return;
  sessionDetailCache.steps.forEach(t => selected.add(t.step_index));
  renderSteps();
  renderSelection();
}

function clearSel() {
  selected.clear();
  renderSteps();
  renderSelection();
}

// ── Copy ──
function showToast(msg) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.style.display = "block";
  setTimeout(() => { toast.style.display = "none"; toast.textContent = "Скопировано"; }, 1100);
}

function copyText(txt) {
  navigator.clipboard.writeText(txt);
  showToast("Скопировано");
}

function copyProjectPath() {
  const p = currentProject();
  copyText(p ? p.path : "");
}

function summary(title, steps) {
  const z = totals(steps);
  const ratio = z.input ? z.cached / z.input : 0;
  const p = currentProject();
  const models = [...new Set(steps.map(t => t.model))].join(", ") || "-";
  return `${title}
Project: ${p ? p.name : ""}
Project path: ${p ? p.path : ""}
Session: ${currentSessionId}
Steps: ${steps.length}
Models: ${models}
Total cost: ${money(z.cost)}
Total input: ${z.input}
Total cached: ${z.cached}
Total non-cached: ${z.non}
Cache ratio: ${pct(ratio)}
Total output: ${z.output}
Total reasoning: ${z.reasoning}
Warnings: ${z.warnings}`;
}

function table(steps) {
  const rows = [
    "| Step | Model | Cost | Input | Cached | Non-cached | Cache | Output | Reasoning | Prompt | Answer |",
    "|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|"
  ];
  steps.forEach(t => {
    const u = t.usage || {};
    rows.push(`| ${t.step_index} | ${t.model} | ${money(u.estimated_total_cost_usd)} | ${u.input_tokens} | ${u.cached_tokens} | ${u.non_cached_input_tokens} | ${pct(u.cached_ratio)} | ${u.output_tokens} | ${u.reasoning_tokens} | ${t.user_prompt.available ? "yes" : "no"} | ${t.assistant_answer.available ? "yes" : "no"} |`);
  });
  return rows.join("\n");
}

function copyStepSummary(i) {
  const s = sessionDetailCache;
  if (!s || !s.steps) return;
  copyText(summary("Step summary", s.steps.filter(t => t.step_index === i)));
}

function copySessionSummary() {
  const s = sessionDetailCache;
  if (!s || !s.steps) return;
  copyText(summary("Session summary", s.steps));
}

function copySessionJson() {
  copyText(JSON.stringify(sessionDetailCache, null, 2));
}

function copySessionTable() {
  const s = sessionDetailCache;
  if (!s || !s.steps) return;
  copyText(table(s.steps));
}

function copySelectedSummary() {
  copyText(summary("Selected steps", selectedSteps()));
}

function copySelectedJson() {
  copyText(JSON.stringify(selectedSteps(), null, 2));
}

function copySelectedTable() {
  copyText(table(selectedSteps()));
}

// ── Auto refresh ──
function toggleAutoRefresh() {
  autoRefresh = !autoRefresh;
  renderStatus();
  setupAutoRefresh();
}

function setupAutoRefresh() {
  if (refreshTimer) clearInterval(refreshTimer);
  if (autoRefresh && !stopped) {
    refreshTimer = setInterval(() => {
      refreshAll();
    }, 3000);
  }
}

// ── Controls collapse ──
function toggleControls() {
  const wrap = document.getElementById("controlsWrap");
  const btn = document.getElementById("collapseBtn");
  wrap.classList.toggle("collapsed");
  btn.textContent = wrap.classList.contains("collapsed") ? "▸" : "▾";
  localStorage.setItem("ctm_controls_collapsed", wrap.classList.contains("collapsed") ? "1" : "0");
}

// ── Resizer ──
function setupResizer() {
  const app = document.getElementById("app");
  const resizer = document.getElementById("resizer");
  let dragging = false;
  resizer.addEventListener("mousedown", () => {
    dragging = true;
    document.body.style.userSelect = "none";
  });
  window.addEventListener("mousemove", e => {
    if (!dragging) return;
    const w = Math.max(280, Math.min(620, e.clientX));
    app.style.setProperty("--left-width", w + "px");
    localStorage.setItem("ctm_left_width", String(w));
  });
  window.addEventListener("mouseup", () => {
    dragging = false;
    document.body.style.userSelect = "";
  });
}

// ── Event listeners ──
document.getElementById("projectSelect").addEventListener("change", async e => {
  currentProjectId = e.target.value;
  currentSessionId = "";
  selected.clear();
  await refreshAll();
});

["q", "modelFilter", "riskFilter"].forEach(id =>
  document.getElementById(id).addEventListener("input", () => {
    renderSessions();
  })
);

document.getElementById("modelFilter").addEventListener("change", () => renderSessions());
document.getElementById("riskFilter").addEventListener("change", () => renderSessions());

// ── Init ──
function loadUIState() {
  showArchived = localStorage.getItem("ctm_show_archived") === "1";
  const collapsed = localStorage.getItem("ctm_controls_collapsed") === "1";
  if (collapsed) {
    document.getElementById("controlsWrap").classList.add("collapsed");
    document.getElementById("collapseBtn").textContent = "▸";
  }
  const left = localStorage.getItem("ctm_left_width");
  if (left) document.getElementById("app").style.setProperty("--left-width", left + "px");
}

async function init() {
  loadUIState();
  setupResizer();
  setupAutoRefresh();
  await refreshAll();
}

init();
