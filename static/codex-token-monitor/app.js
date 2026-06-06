"use strict";

// ── State ──
let currentSourceId = "";
let currentSessionId = "";
let selected = new Set();
let autoRefresh = true;
let stopped = false;
let showArchived = false;
let refreshTimer = null;
let refreshPromise = null;
const MIN_VISIBLE_SESSION_DATE_MS = Date.parse("2026-06-04T00:00:00Z");
const ALL_WORKDIRS_VALUE = "";

// ── Data caches ──
let sourcesCache = [];
let sessionsCache = [];
let sessionDetailCache = null;
let sessionDetailLoading = false;
let statusCache = { collector: "unknown", prompt_logging: true, last_update: "" };
let currentWorkdirFilter = ALL_WORKDIRS_VALUE;

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
async function loadSources() {
  const data = await api("/api/sources");
  if (data && data.sources) {
    sourcesCache = data.sources;
    if (!currentSourceId && data.default_source_id) {
      currentSourceId = data.default_source_id;
    }
    if (!currentSourceId && sourcesCache.length > 0) {
      currentSourceId = sourcesCache[0].id;
    }
  }
  if (sourcesCache.length > 0 && !currentSourceId) {
    currentSourceId = sourcesCache[0].id;
  }
}

function currentSource() {
  return sourcesCache.find(s => s.id === currentSourceId) || sourcesCache[0] || null;
}

function normalizeWorkdir(raw) {
  let text = String(raw || "").trim();
  if (!text) return "";
  if (text.startsWith("\\\\?\\")) text = text.slice(4);
  return text.replaceAll("/", "\\");
}

function projectLabelFromWorkdir(raw) {
  const workdir = normalizeWorkdir(raw);
  if (!workdir) return "Без папки";
  const parts = workdir.split("\\").filter(Boolean);
  return parts[parts.length - 1] || workdir;
}

function sessionTimestampMs(session) {
  const raw = session?.date;
  if (typeof raw === "number") return raw > 1_000_000_000_000 ? raw : raw * 1000;
  const num = Number(raw);
  if (Number.isFinite(num) && raw !== "" && raw != null) {
    return num > 1_000_000_000_000 ? num : num * 1000;
  }
  const parsed = Date.parse(String(raw || ""));
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatSessionDate(session) {
  const ts = sessionTimestampMs(session);
  if (!ts) return "дата неизвестна";
  return new Date(ts).toLocaleString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function workdirChoices() {
  const seen = new Map();
  sessionsCache.forEach(session => {
    const value = normalizeWorkdir(session.workdir);
    if (!value || seen.has(value)) return;
    seen.set(value, {
      value,
      label: projectLabelFromWorkdir(value),
    });
  });
  return [...seen.values()].sort((a, b) => a.label.localeCompare(b.label, "ru"));
}

function preferredSessionId(list) {
  const sessions = list || [];
  const withSteps = sessions.find(s => Number(s.step_count || 0) > 0);
  return (withSteps || sessions[0] || {}).id || "";
}

async function loadSessions() {
  if (!currentSourceId) { sessionsCache = []; return; }
  const data = await api("/api/sessions?source_id=" + encodeURIComponent(currentSourceId) +
    "&show_archived=" + (showArchived ? "1" : "0"));
  if (data && data.sessions) {
    sessionsCache = data.sessions;
  } else {
    sessionsCache = [];
  }
  if (sessionsCache.length > 0 && !currentSessionId) {
    currentSessionId = preferredSessionId(sessionsCache);
  }
  if (!sessionsCache.find(s => s.id === currentSessionId)) {
    currentSessionId = preferredSessionId(sessionsCache);
  }
}

async function loadSessionDetail() {
  if (!currentSourceId || !currentSessionId) {
    sessionDetailCache = null;
    sessionDetailLoading = false;
    return;
  }
  sessionDetailLoading = true;
  const data = await api("/api/session?source_id=" + encodeURIComponent(currentSourceId) +
    "&session_id=" + encodeURIComponent(currentSessionId));
  sessionDetailCache = data;
  sessionDetailLoading = false;
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
  if (refreshPromise) {
    return refreshPromise;
  }
  refreshPromise = (async () => {
    await loadSources();
    initSources();
    await loadSessions();
    if (!sessionDetailCache) {
      const preferredId = preferredSessionId(sessionsCache);
      if (preferredId) currentSessionId = preferredId;
    }
    await loadStatus();
    populateWorkdirFilter();
    populateModelFilter();
    if (!sessionDetailCache || sessionDetailCache.id !== currentSessionId) {
      sessionDetailCache = null;
    }
    renderAll();
    await loadSessionDetail();
    renderAll();
  })();
  try {
    await refreshPromise;
  } finally {
    refreshPromise = null;
  }
}

async function refreshData() {
  await apiPost("/api/refresh", { source_id: currentSourceId, session_id: currentSessionId });
  document.getElementById("lastUpdate").textContent = new Date().toLocaleTimeString("ru-RU");
  showToast("Данные обновлены");
  await refreshAll();
}

// ── Archive ──
async function toggleArchive(sessionId) {
  const detail = await api("/api/session?source_id=" + encodeURIComponent(currentSourceId) +
    "&session_id=" + encodeURIComponent(sessionId));
  const isArchivedNow = detail && detail.archived;
  await apiPost(isArchivedNow ? "/api/unarchive" : "/api/archive", {
    source_id: currentSourceId,
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
  const sortMode = (document.getElementById("sortFilter")?.value || "date_desc");
  const workdirFilter = normalizeWorkdir(document.getElementById("workdirFilter")?.value || currentWorkdirFilter || "");
  const list = sessionsCache.filter(s => {
    const ts = sessionTimestampMs(s);
    if (ts && ts < MIN_VISIBLE_SESSION_DATE_MS) return false;
    const sessionWorkdir = normalizeWorkdir(s.workdir);
    const txt = (s.title + " " + s.id + " " + s.model + " " + s.reasoning + " " + s.workdir).toLowerCase();
    const hasWarn = s.warnings_count > 0;
    return txt.includes(q) &&
      (!workdirFilter || sessionWorkdir === workdirFilter) &&
      (!mf || s.model === mf) &&
      (!rf || (rf === "warnings" ? hasWarn : !hasWarn));
  });
  list.sort((a, b) => {
    const aDate = sessionTimestampMs(a);
    const bDate = sessionTimestampMs(b);
    const aCost = Number(a.total_cost_usd || 0);
    const bCost = Number(b.total_cost_usd || 0);
    switch (sortMode) {
      case "date_asc":
        return aDate - bDate;
      case "cost_desc":
        return bCost - aCost || bDate - aDate;
      case "cost_asc":
        return aCost - bCost || bDate - aDate;
      case "date_desc":
      default:
        return bDate - aDate;
    }
  });
  return list;
}

function currentSession() {
  return filteredSessions().find(s => s.id === currentSessionId) || filteredSessions()[0] || null;
}

function totals(steps) {
  return steps.reduce((a, t) => {
    // Only sum per-step usage when available (not ambiguous/cumulative)
    const u = t.usage || {};
    if (u.available !== false) {
      a.input += u.input_tokens || 0;
      a.cached += u.cached_tokens || 0;
      a.non += u.non_cached_input_tokens || 0;
      a.output += u.output_tokens || 0;
      a.reasoning += u.reasoning_tokens || 0;
      a.tool += u.tool_tokens || 0;
      a.cost += u.estimated_total_cost_usd || 0;
    }
    a.warnings += (t.warnings || []).length;
    return a;
  }, { input: 0, cached: 0, non: 0, output: 0, reasoning: 0, tool: 0, cost: 0, warnings: 0 });
}

function metricsForSession(session) {
  const summary = session?.summary || null;
  if (summary && (
    summary.total_input_tokens ||
    summary.total_cached_tokens ||
    summary.total_output_tokens ||
    summary.estimated_total_cost_usd
  )) {
    return {
      input: summary.total_input_tokens || 0,
      cached: summary.total_cached_tokens || 0,
      non: summary.total_non_cached_input_tokens || 0,
      output: summary.total_output_tokens || 0,
      reasoning: summary.total_reasoning_tokens || 0,
      tool: summary.total_tool_tokens || 0,
      cost: summary.estimated_total_cost_usd || 0,
      warnings: (summary.warnings || []).length,
      ratio: summary.average_cached_ratio || 0,
      turnCount: summary.turn_count || 0,
    };
  }
  const z = totals(session?.steps || []);
  return {
    ...z,
    ratio: z.input ? z.cached / z.input : 0,
    turnCount: (session?.steps || []).length,
  };
}

// ── Render: left panel ──
function initSources() {
  const sel = document.getElementById("sourceSelect");
  if (!sel) return;
  sel.innerHTML = sourcesCache.map(s =>
    `<option value="${s.id}">${s.name} (${s.kind === 'live' ? 'live' : 'архив'})</option>`
  ).join("");
  sel.value = currentSourceId;
}

function renderSourceInfo() {
  const s = currentSource();
  const selectedPath = currentWorkdirFilter || "";
  const fallback = s ? (s.kind === "live" ? "C:/Users/andre/.codex" : "D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger") : "";
  document.getElementById("sourcePath").textContent = selectedPath || fallback;
}

function populateWorkdirFilter() {
  const sel = document.getElementById("workdirFilter");
  if (!sel) return;
  const previousValue = currentWorkdirFilter || sel.value || ALL_WORKDIRS_VALUE;
  const choices = workdirChoices();
  sel.innerHTML = `<option value="${ALL_WORKDIRS_VALUE}">Все проекты / папки</option>`;
  choices.forEach(choice => {
    sel.innerHTML += `<option value="${escapeHtml(choice.value)}">${escapeHtml(choice.label)}</option>`;
  });
  const valid = new Set([ALL_WORKDIRS_VALUE, ...choices.map(choice => choice.value)]);
  currentWorkdirFilter = valid.has(previousValue) ? previousValue : ALL_WORKDIRS_VALUE;
  sel.value = currentWorkdirFilter;
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

  if (!list.find(s => s.id === currentSessionId)) currentSessionId = preferredSessionId(list);

  list.forEach(s => {
    const costText = s.total_cost_usd == null ? "—" : money(s.total_cost_usd);
    const stepText = s.step_count == null ? "—" : nf.format(s.step_count);
    const el = document.createElement("div");
    const sourceKind = s.source_kind || "archive";
    const badgeCls = sourceKind === "live" ? "green" : "purple";
    const sourceLabel = sourceKind === "live" ? "live" : "архив";

    // Confirmation badges
    const cbadges = (s.confirmation_badges || []).map(b => `<span class="pill yellow">${b}</span>`).join("");

    el.className = "session" + (s.id === currentSessionId ? " active" : "");
    el.onclick = async () => {
      currentSessionId = s.id;
      selected.clear();
      sessionDetailCache = null;
      sessionDetailLoading = true;
      renderAll();
      await loadSessionDetail();
      renderAll();
    };
    el.innerHTML = `
      <div class="session-head">
        <div>
          <div class="session-title">${escapeHtml(s.title)}</div>
          <div class="session-id muted xsmall mono">${escapeHtml(s.id)}</div>
          <div class="session-date">${escapeHtml(formatSessionDate(s))}</div>
        </div>
        <div class="row-actions">
          <button class="icon ghost" title="Архивировать/Вернуть" onclick="event.stopPropagation();toggleArchive('${s.id}')">🗄</button>
          <span class="pill blue">${stepText}</span>
        </div>
      </div>
      <div class="pills">
        <span class="pill ${badgeCls}">${sourceLabel}</span>
        <span class="pill">${escapeHtml(s.model)}</span>
        <span class="pill purple">${escapeHtml(s.reasoning)}</span>
        <span class="pill ${s.warnings_count ? 'yellow' : 'green'}">${s.warnings_count} warn</span>
        ${cbadges}
        ${s.has_normalized ? '<span class="pill green">normalized</span>' : (s.has_parsed ? '<span class="pill">parsed</span>' : '')}
      </div>
      <div class="compact-metrics">
        <div class="cmini"><span>Cost</span><b>${costText}</b></div>
        <div class="cmini"><span>Steps</span><b>${stepText}</b></div>
        <div class="cmini"><span>Model</span><b>${escapeHtml(s.model)}</b></div>
      </div>`;
    root.appendChild(el);
  });
}

// ── Render: header ──
function stat(label, value, cls) {
  return `<div class="stat ${cls || ""}"><label>${label}</label><b>${value}</b></div>`;
}

function usageNumber(usage, key) {
  if (!usage || usage.available === false) return "—";
  return nf.format(usage[key] || 0);
}

function usageMoney(usage, key) {
  if (!usage || usage.available === false) return "—";
  const value = usage[key];
  return value == null ? "—" : money(value);
}

function usagePercent(usage, key) {
  if (!usage || usage.available === false) return "—";
  return pct(usage[key] || 0);
}

function renderHeader() {
  const s = sessionDetailCache;
  if (!s) {
    document.getElementById("title").textContent = "Выберите сессию";
    const selectedSession = currentSession();
    document.getElementById("title").textContent = selectedSession ? "Загрузка сессии..." : document.getElementById("title").textContent;
    document.getElementById("meta").textContent = selectedSession ? selectedSession.title : "";
    document.getElementById("stats").innerHTML = "";
    return;
  }
  const z = metricsForSession(s);
  const src = currentSource();
  const sourceKind = s.source_kind || "archive";
  const kindLabel = sourceKind === "live" ? "live" : "архив";

  const hasAmbiguousLiveSteps = sourceKind === "live" && (s.steps || []).some(t => t?.usage?.available === false);
  const usageNote = hasAmbiguousLiveSteps ? " · часть шагов без точной per-step разбивки" : "";

  document.getElementById("title").textContent = s.title;
  document.getElementById("meta").textContent = `${src ? src.name : ""} [${kindLabel}] · ${s.id} · ${s.date} · ${s.workdir}${usageNote}`;
  document.getElementById("stats").innerHTML = [
    stat("Cost", money(z.cost), "good"),
    stat("Input", nf.format(z.input), "blue"),
    stat("Cached", nf.format(z.cached), "good"),
    stat("Non-cached", nf.format(z.non), "warn"),
    stat("Cache", pct(z.ratio), "blue"),
    stat("Output", nf.format(z.output)),
  ].join("");
}

// ── Render: steps ──
function metric(label, value) { return `<div class="metric"><span>${label}</span><b>${value}</b></div>`; }
function kv(k, v) { return `<div class="kv"><span class="muted">${k}</span><span class="mono">${String(v)}</span></div>`; }
function escapeHtml(t) { return String(t || "").replace(/[&<>\"']/g, m => ({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;" }[m])); }
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

function renderTimelineEvent(evt) {
  const ids = [];
  if (evt.compaction_task_id) ids.push(`task: ${escapeHtml(evt.compaction_task_id)}`);
  if (evt.after_step_turn_id) ids.push(`step turn: ${escapeHtml(evt.after_step_turn_id)}`);
  return `
    <div class="timeline-event">
      <div class="timeline-head">
        <span class="pill yellow">timeline</span>
        <b>${escapeHtml(evt.label || evt.event_type || "event")}</b>
        <span class="muted">${evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString("ru-RU") : ""}</span>
      </div>
      <div class="timeline-body">
        <span class="muted">После шага ${evt.after_step_index || "?"}</span>
        ${ids.length ? `<span class="mono">${ids.join(" · ")}</span>` : ""}
      </div>
    </div>`;
}

function renderSteps() {
  const root = document.getElementById("steps");
  root.innerHTML = "";
  const s = sessionDetailCache;
  if (!s || !s.steps || !s.steps.length) {
    root.innerHTML = `<div class="loading">${currentSession() ? "Загрузка шагов..." : "Нет данных по шагам"}</div>`;
    return;
  }

  // Source kind indicator
  const sourceKind = s.source_kind || "archive";
  const hasAmbiguousLiveSteps = sourceKind === "live" && s.steps.some(t => t?.usage?.available === false);
  const usageWarning = hasAmbiguousLiveSteps
    ? `<div class="empty small" style="margin-bottom:8px">⚠ Для части live-шагов точная per-step разбивка не подтверждена. В таких местах смотри totals всей сессии.</div>`
    : "";

  if (usageWarning) {
    const warnEl = document.createElement("div");
    warnEl.innerHTML = usageWarning;
    root.appendChild(warnEl);
  }

  const timelineByStep = new Map();
  (s.timeline_events || []).forEach(evt => {
    const key = Number(evt.after_step_index || 0);
    if (!timelineByStep.has(key)) timelineByStep.set(key, []);
    timelineByStep.get(key).push(evt);
  });

  s.steps.forEach(t => {
    const el = document.createElement("div");
    const idx = t.step_index;
    el.className = "step" + (selected.has(idx) ? " selected" : "");
    el.id = "step-" + idx;
    const u = t.usage || {};
    const env = t.environment || {};
    const usageAvail = u.available !== false;
    const usageNote = (!usageAvail && u.note) ? `<span class="muted xsmall"> (${u.note})</span>` : "";
    const postBadges = (t.post_step_badges || []).map(b => `<span class="pill yellow">${escapeHtml(b)}</span>`).join("");

    el.innerHTML = `
      <div class="step-head" onclick="toggleDetails(${idx})">
        <input type="checkbox" ${selected.has(idx) ? "checked" : ""} onclick="event.stopPropagation()" onchange="toggleSelect(${idx})">
        <div>
          <div class="step-title">
            <b>Step ${idx}</b>
            <span class="pill blue">${escapeHtml(t.model)}</span>
            <span class="pill purple">${escapeHtml(t.reasoning_effort)}</span>
            ${usageAvail ? '' : '<span class="pill yellow" title="Для этого шага нет подтвержденной per-step token delta">usage⚠</span>'}
            <span class="pill ${(t.warnings || []).length ? 'yellow' : 'green'}">${(t.warnings || []).length} warn</span>
            ${postBadges}
          </div>
          <div class="metrics">
            ${metric("Cost", usageMoney(u, "estimated_total_cost_usd"))}
            ${metric("Input", usageNumber(u, "input_tokens"))}
            ${metric("Cached", usageNumber(u, "cached_tokens"))}
            ${metric("Non-cached", usageNumber(u, "non_cached_input_tokens"))}
            ${metric("Cache", usagePercent(u, "cached_ratio"))}
            ${metric("Output", usageNumber(u, "output_tokens"))}
            ${metric("Reasoning", usageNumber(u, "reasoning_tokens"))}
            ${metric("MCP", nf.format(env.observed_mcp_server_count))}
          </div>
          <div class="preview-row">
            <div class="preview">
              <span class="label">${t.user_prompt.kind === 'system_composed' ? 'System prompt' : 'Prompt'}</span>
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
        ${textBlock(t.user_prompt.kind === 'system_composed' ? "System prompt (composed)" : "User prompt", "prompt", t.user_prompt.available, t.user_prompt.text, idx)}
        ${textBlock("Assistant answer", "answer", t.assistant_answer.available, t.assistant_answer.text, idx)}
        <div class="detail-grid">
          <div class="box">
            <h3>Tokens${usageNote}</h3>
            ${kv("input_tokens", usageNumber(u, "input_tokens"))}
            ${kv("cached_tokens", usageNumber(u, "cached_tokens"))}
            ${kv("non_cached", usageNumber(u, "non_cached_input_tokens"))}
            ${kv("cached_ratio", usagePercent(u, "cached_ratio"))}
            ${kv("output_tokens", usageNumber(u, "output_tokens"))}
            ${kv("reasoning_tokens", usageNumber(u, "reasoning_tokens"))}
            ${kv("tool_tokens", usageNumber(u, "tool_tokens"))}
          </div>
          <div class="box">
            <h3>Cost</h3>
            ${kv("input_cost", usageMoney(u, "estimated_input_cost_usd"))}
            ${kv("cached_cost", usageMoney(u, "estimated_cached_input_cost_usd"))}
            ${kv("output_cost", usageMoney(u, "estimated_output_cost_usd"))}
            ${kv("total_cost", usageMoney(u, "estimated_total_cost_usd"))}
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
  renderSourceInfo();
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

function copySourcePath() {
  const s = currentSource();
  const selectedPath = currentWorkdirFilter || "";
  copyText(selectedPath || (s ? (s.kind === "live" ? "C:/Users/andre/.codex" : "D:/Codex+Kilocode/projects/sword-of-rome-web/_local/codex-token-debugger") : ""));
}

function summary(title, steps, metricsOverride = null) {
  const z = metricsOverride || totals(steps);
  const ratio = metricsOverride ? (metricsOverride.ratio || 0) : (z.input ? z.cached / z.input : 0);
  const src = currentSource();
  const models = [...new Set(steps.map(t => t.model))].join(", ") || "-";
  return `${title}
Source: ${src ? src.name : ""}
Source ID: ${currentSourceId}
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
    rows.push(`| ${t.step_index} | ${t.model} | ${usageMoney(u, "estimated_total_cost_usd")} | ${usageNumber(u, "input_tokens")} | ${usageNumber(u, "cached_tokens")} | ${usageNumber(u, "non_cached_input_tokens")} | ${usagePercent(u, "cached_ratio")} | ${usageNumber(u, "output_tokens")} | ${usageNumber(u, "reasoning_tokens")} | ${t.user_prompt.available ? "yes" : "no"} | ${t.assistant_answer.available ? "yes" : "no"} |`);
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
  copyText(summary("Session summary", s.steps, metricsForSession(s)));
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

async function applySessionFilters() {
  const previousSessionId = currentSessionId;
  renderSessions();
  renderSourceInfo();
  if (currentSessionId !== previousSessionId) {
    selected.clear();
    sessionDetailCache = null;
    sessionDetailLoading = true;
    renderAll();
    await loadSessionDetail();
    renderAll();
    return;
  }
  renderHeader();
  renderSteps();
  renderSelection();
}

function renderHeader() {
  const s = sessionDetailCache;
  if (!s) {
    document.getElementById("title").textContent = "Выберите сессию";
    const selectedSession = currentSession();
    document.getElementById("title").textContent = selectedSession && sessionDetailLoading
      ? "Загрузка сессии..."
      : document.getElementById("title").textContent;
    document.getElementById("meta").textContent = selectedSession ? selectedSession.title : "";
    document.getElementById("stats").innerHTML = "";
    return;
  }
  const z = metricsForSession(s);
  const src = currentSource();
  const sourceKind = s.source_kind || "archive";
  const kindLabel = sourceKind === "live" ? "live" : "архив";
  const hasAmbiguousLiveSteps = sourceKind === "live" && (s.steps || []).some(t => t?.usage?.available === false);
  const usageNote = hasAmbiguousLiveSteps ? " · часть шагов без точной per-step разбивки" : "";

  document.getElementById("title").textContent = s.title;
  document.getElementById("meta").textContent = `${src ? src.name : ""} [${kindLabel}] · ${s.id} · ${s.date} · ${s.workdir}${usageNote}`;
  document.getElementById("stats").innerHTML = [
    stat("Cost", money(z.cost), "good"),
    stat("Input", nf.format(z.input), "blue"),
    stat("Cached", nf.format(z.cached), "good"),
    stat("Non-cached", nf.format(z.non), "warn"),
    stat("Cache", pct(z.ratio), "blue"),
    stat("Output", nf.format(z.output)),
  ].join("");
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

  if (!list.find(s => s.id === currentSessionId)) currentSessionId = preferredSessionId(list);

  list.forEach(s => {
    const costText = s.total_cost_usd == null ? "—" : money(s.total_cost_usd);
    const stepText = s.step_count == null ? "—" : nf.format(s.step_count);
    const el = document.createElement("div");
    const sourceKind = s.source_kind || "archive";
    const badgeCls = sourceKind === "live" ? "green" : "purple";
    const sourceLabel = sourceKind === "live" ? "live" : "архив";
    const cbadges = (s.confirmation_badges || []).map(b => `<span class="pill yellow">${b}</span>`).join("");

    el.className = "session" + (s.id === currentSessionId ? " active" : "");
    el.onclick = async () => {
      currentSessionId = s.id;
      selected.clear();
      sessionDetailCache = null;
      sessionDetailLoading = true;
      renderAll();
      await loadSessionDetail();
      renderAll();
    };
    el.innerHTML = `
      <div class="session-head">
        <div>
          <div class="session-title">${escapeHtml(s.title)}</div>
          <div class="session-id muted xsmall mono">${escapeHtml(s.id)}</div>
          <div class="session-date">${escapeHtml(formatSessionDate(s))}</div>
        </div>
        <div class="row-actions">
          <button class="icon ghost" title="Архивировать/Вернуть" onclick="event.stopPropagation();toggleArchive('${s.id}')">🗄</button>
          <span class="pill blue">${stepText}</span>
        </div>
      </div>
      <div class="pills">
        <span class="pill ${badgeCls}">${sourceLabel}</span>
        <span class="pill">${escapeHtml(s.model)}</span>
        <span class="pill purple">${escapeHtml(s.reasoning)}</span>
        <span class="pill ${s.warnings_count ? 'yellow' : 'green'}">${s.warnings_count} warn</span>
        ${cbadges}
        ${s.has_normalized ? '<span class="pill green">normalized</span>' : (s.has_parsed ? '<span class="pill">parsed</span>' : '')}
      </div>
      <div class="compact-metrics">
        <div class="cmini"><span>Cost</span><b>${costText}</b></div>
        <div class="cmini"><span>Steps</span><b>${stepText}</b></div>
        <div class="cmini"><span>Model</span><b>${escapeHtml(s.model)}</b></div>
      </div>`;
    root.appendChild(el);
  });
}

function renderSteps() {
  const root = document.getElementById("steps");
  root.innerHTML = "";
  const s = sessionDetailCache;
  if (!s) {
    root.innerHTML = `<div class="loading">${currentSession() && sessionDetailLoading ? "Загрузка шагов..." : "Выберите сессию слева"}</div>`;
    return;
  }
  if (!s.steps || !s.steps.length) {
    root.innerHTML = `<div class="loading">Для этой сессии шаги пока не найдены</div>`;
    return;
  }

  const sourceKind = s.source_kind || "archive";
  const hasAmbiguousLiveSteps = sourceKind === "live" && s.steps.some(t => t?.usage?.available === false);
  const usageWarning = hasAmbiguousLiveSteps
    ? `<div class="empty small" style="margin-bottom:8px">⚠ Для части live-шагов точная per-step разбивка не подтверждена. В таких местах смотри totals всей сессии.</div>`
    : "";

  if (usageWarning) {
    const warnEl = document.createElement("div");
    warnEl.innerHTML = usageWarning;
    root.appendChild(warnEl);
  }

  const timelineByStep = new Map();
  (s.timeline_events || []).forEach(evt => {
    const key = Number(evt.after_step_index || 0);
    if (!timelineByStep.has(key)) timelineByStep.set(key, []);
    timelineByStep.get(key).push(evt);
  });

  s.steps.forEach(t => {
    const el = document.createElement("div");
    const idx = t.step_index;
    el.className = "step" + (selected.has(idx) ? " selected" : "");
    el.id = "step-" + idx;
    const u = t.usage || {};
    const env = t.environment || {};
    const usageAvail = u.available !== false;
    const usageNote = (!usageAvail && u.note) ? `<span class="muted xsmall"> (${u.note})</span>` : "";
    const postBadges = (t.post_step_badges || []).map(b => `<span class="pill yellow">${escapeHtml(b)}</span>`).join("");

    el.innerHTML = `
      <div class="step-head" onclick="toggleDetails(${idx})">
        <input type="checkbox" ${selected.has(idx) ? "checked" : ""} onclick="event.stopPropagation()" onchange="toggleSelect(${idx})">
        <div>
          <div class="step-title">
            <b>Step ${idx}</b>
            <span class="pill blue">${escapeHtml(t.model)}</span>
            <span class="pill purple">${escapeHtml(t.reasoning_effort)}</span>
            ${usageAvail ? '' : '<span class="pill yellow" title="Для этого шага нет подтвержденной per-step token delta">usage⚠</span>'}
            <span class="pill ${(t.warnings || []).length ? 'yellow' : 'green'}">${(t.warnings || []).length} warn</span>
            ${postBadges}
          </div>
          <div class="metrics">
            ${metric("Cost", usageMoney(u, "estimated_total_cost_usd"))}
            ${metric("Input", usageNumber(u, "input_tokens"))}
            ${metric("Cached", usageNumber(u, "cached_tokens"))}
            ${metric("Non-cached", usageNumber(u, "non_cached_input_tokens"))}
            ${metric("Cache", usagePercent(u, "cached_ratio"))}
            ${metric("Output", usageNumber(u, "output_tokens"))}
            ${metric("Reasoning", usageNumber(u, "reasoning_tokens"))}
            ${metric("MCP", nf.format(env.observed_mcp_server_count))}
          </div>
          <div class="preview-row">
            <div class="preview">
              <span class="label">${t.user_prompt.kind === 'system_composed' ? 'System prompt' : 'Prompt'}</span>
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
        ${textBlock(t.user_prompt.kind === 'system_composed' ? "System prompt (composed)" : "User prompt", "prompt", t.user_prompt.available, t.user_prompt.text, idx)}
        ${textBlock("Assistant answer", "answer", t.assistant_answer.available, t.assistant_answer.text, idx)}
        <div class="detail-grid">
          <div class="box">
            <h3>Tokens${usageNote}</h3>
            ${kv("input_tokens", usageNumber(u, "input_tokens"))}
            ${kv("cached_tokens", usageNumber(u, "cached_tokens"))}
            ${kv("non_cached", usageNumber(u, "non_cached_input_tokens"))}
            ${kv("cached_ratio", usagePercent(u, "cached_ratio"))}
            ${kv("output_tokens", usageNumber(u, "output_tokens"))}
            ${kv("reasoning_tokens", usageNumber(u, "reasoning_tokens"))}
            ${kv("tool_tokens", usageNumber(u, "tool_tokens"))}
          </div>
          <div class="box">
            <h3>Cost</h3>
            ${kv("input_cost", usageMoney(u, "estimated_input_cost_usd"))}
            ${kv("cached_cost", usageMoney(u, "estimated_cached_input_cost_usd"))}
            ${kv("output_cost", usageMoney(u, "estimated_output_cost_usd"))}
            ${kv("total_cost", usageMoney(u, "estimated_total_cost_usd"))}
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

    const extraEvents = timelineByStep.get(Number(idx)) || [];
    extraEvents.forEach(evt => {
      const wrap = document.createElement("div");
      wrap.innerHTML = renderTimelineEvent(evt);
      root.appendChild(wrap.firstElementChild);
    });
  });
}

// ── Event listeners ──
document.getElementById("sourceSelect").addEventListener("change", async e => {
  currentSourceId = e.target.value;
  currentWorkdirFilter = ALL_WORKDIRS_VALUE;
  localStorage.removeItem("ctm_workdir_filter");
  currentSessionId = "";
  selected.clear();
  await refreshAll();
});

document.getElementById("workdirFilter").addEventListener("change", async e => {
  currentWorkdirFilter = normalizeWorkdir(e.target.value || "");
  localStorage.setItem("ctm_workdir_filter", currentWorkdirFilter);
  await applySessionFilters();
});

document.getElementById("q").addEventListener("input", async () => {
  await applySessionFilters();
});

document.getElementById("modelFilter").addEventListener("change", async () => {
  await applySessionFilters();
});
document.getElementById("riskFilter").addEventListener("change", async () => {
  await applySessionFilters();
});
document.getElementById("sortFilter").addEventListener("change", async e => {
  localStorage.setItem("ctm_sort_mode", e.target.value);
  await applySessionFilters();
});

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
  const sort = localStorage.getItem("ctm_sort_mode");
  if (sort) {
    const sortEl = document.getElementById("sortFilter");
    if (sortEl) sortEl.value = sort;
  }
  currentWorkdirFilter = normalizeWorkdir(localStorage.getItem("ctm_workdir_filter") || "");
}

async function init() {
  loadUIState();
  setupResizer();
  setupAutoRefresh();
  initSources();
  await refreshAll();
}

init();
