import React, { useEffect, useMemo, useState } from "react";
import {
  Search,
  Plus,
  RefreshCw,
  Play,
  Square,
  ExternalLink,
  FolderOpen,
  Trash2,
  Settings,
  Archive,
  Map,
  Layers3,
  PanelRight,
  Gamepad2,
  Boxes,
  TerminalSquare,
  Check,
  X,
  MonitorPlay,
  Tags,
  Clock3,
  Pencil,
  SlidersHorizontal,
  Save,
  Hash,
  ChevronDown,
  Grid2X2,
  List,
  Columns3,
  Star,
  Copy,
  MoreHorizontal,
  Server,
  Database,
  Menu,
  PanelLeftClose,
  Shield,
  Swords,
} from "lucide-react";

const initialCategories = [
  "Карты",
  "Фишки",
  "Карты событий",
  "Панели",
  "Полные прототипы",
  "Архив",
];

const initialProjects = [
  {
    id: "italia-antiqua-table",
    title: "Italia Antiqua — Digital Table",
    description: "Интерактивный стол для античных сражений",
    longDescription:
      "Полноценный цифровой стол для игры в античные сражения. Поддержка юнитов, зон контроля, инициативы, карточек событий и логов.",
    type: "Полные прототипы",
    status: "running",
    port: 5173,
    stack: "Vite + React + TS",
    path: "D:\Arena\Prototypes\italia-antiqua",
    tags: ["Полный прототип", "Античность", "Стол", "Canvas"],
    updated: "Сегодня",
    favorite: true,
    preview: "map",
  },
  {
    id: "counter-drag-test",
    title: "Counter Drag Test",
    description: "Тест перетаскивания и стекования фишек",
    longDescription:
      "Проверка drag-and-drop поведения, выделения активной фишки, стекования, подсветки доступных зон и отката действия.",
    type: "Фишки",
    status: "starting",
    port: 5174,
    stack: "React Canvas",
    path: "D:\Arena\Prototypes\counter-drag-test",
    tags: ["Фишки", "UX", "Тест"],
    updated: "Вчера",
    favorite: false,
    preview: "dice",
  },
  {
    id: "card-hand-ui",
    title: "Card Hand UI",
    description: "Интерфейс рук карт с анимациями",
    longDescription:
      "Прототип карточной руки: наведение, выбор карты, раскрытие события, быстрые действия, сброс и анимация применения эффекта.",
    type: "Карты событий",
    status: "stopped",
    port: 5175,
    stack: "Vite + React",
    path: "D:\Arena\Prototypes\card-hand-ui",
    tags: ["Карты", "UI", "Анимации"],
    updated: "2 дня назад",
    favorite: false,
    preview: "cards",
  },
  {
    id: "faction-panel",
    title: "Faction Panel Layout",
    description: "Макет панели фракции и ресурсов",
    longDescription:
      "Панель активной фракции: ресурсы, мораль, очки действий, статус игрока, быстрые кнопки и информационные индикаторы.",
    type: "Панели",
    status: "running",
    port: 5180,
    stack: "React + Tailwind",
    path: "D:\Arena\Prototypes\faction-panel-layout",
    tags: ["Панели", "UI", "Лейаут"],
    updated: "3 дня назад",
    favorite: false,
    preview: "panel",
  },
  {
    id: "turn-tracker-v2",
    title: "Turn Tracker v2",
    description: "Трекер ходов с фазами и таймером",
    longDescription:
      "Проверка компактного трекера ходов: текущий раунд, фаза, активный игрок, завершение хода и визуальный прогресс кампании.",
    type: "Панели",
    status: "stopped",
    port: 5176,
    stack: "React State",
    path: "D:\Arena\Prototypes\turn-tracker-v2",
    tags: ["Панели", "Геймплей", "Таймер"],
    updated: "На этой неделе",
    favorite: true,
    preview: "turns",
  },
  {
    id: "map-hex-prototype",
    title: "Map Hex Prototype",
    description: "Прототип гекс-карты и рельефа",
    longDescription:
      "Тест карты с гексами, рельефом, городами, маршрутами, границами регионов и слоями поверх основного изображения.",
    type: "Карты",
    status: "stopped",
    port: 5177,
    stack: "Canvas + JSON",
    path: "D:\Arena\Prototypes\map-hex-prototype",
    tags: ["Карты", "Гекс", "Карта"],
    updated: "На прошлой неделе",
    favorite: true,
    preview: "hex",
  },
];

const technologyChips = ["Vite", "Vue 3", "TypeScript", "Pinia"];

function iconForCategory(category) {
  const map = {
    "Все проекты": Boxes,
    Карты: Map,
    Фишки: Layers3,
    "Карты событий": Gamepad2,
    Панели: PanelRight,
    "Полные прототипы": MonitorPlay,
    Архив: Archive,
  };
  return map[category] || Tags;
}

function statusLabel(status) {
  return {
    stopped: "Остановлен",
    running: "Запущен",
    starting: "Запускается...",
    error: "Ошибка",
  }[status];
}

function statusStyles(status) {
  return {
    stopped: "bg-slate-100 text-slate-600",
    running: "bg-emerald-100 text-emerald-700",
    starting: "bg-amber-100 text-amber-700",
    error: "bg-rose-100 text-rose-700",
  }[status];
}

function statusDot(status) {
  return {
    stopped: "bg-slate-400",
    running: "bg-emerald-500",
    starting: "bg-amber-500 animate-pulse",
    error: "bg-rose-500",
  }[status];
}

function normalizeTags(value) {
  return value
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean)
    .filter((tag, index, arr) => arr.findIndex((x) => x.toLowerCase() === tag.toLowerCase()) === index);
}

function PreviewArt({ variant = "map", large = false }) {
  const height = large ? "h-32" : "h-28";

  if (variant === "dice") {
    return (
      <div className={`${height} overflow-hidden rounded-xl bg-zinc-900 p-4 text-white`}>
        <div className="grid h-full grid-cols-[1fr_1fr_1.2fr] gap-3">
          <div className="rounded-lg bg-white/8 p-3 text-center">
            <div className="text-[10px] uppercase text-white/50">Attack</div>
            <div className="mt-2 text-3xl font-black">6</div>
          </div>
          <div className="rounded-lg bg-white/8 p-3 text-center">
            <div className="text-[10px] uppercase text-white/50">Defense</div>
            <div className="mt-2 text-3xl font-black">4</div>
          </div>
          <div className="space-y-2 rounded-lg bg-white/8 p-3">
            {["Terrain", "Supply", "Morale"].map((item, index) => (
              <div key={item} className="flex items-center gap-2 text-[10px] text-white/70">
                <span className={`h-2 w-2 rounded-full ${index === 0 ? "bg-orange-500" : index === 1 ? "bg-sky-400" : "bg-lime-500"}`} />
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (variant === "cards") {
    return (
      <div className={`${height} overflow-hidden rounded-xl bg-zinc-950 p-4`}>
        <div className="flex h-full items-end justify-center gap-3">
          {["Legion", "Cavalry", "Archer", "Engineer"].map((card, index) => (
            <div key={card} className="h-20 w-14 rounded-md border border-amber-900/40 bg-stone-300 p-1 shadow-md">
              <div className="h-10 rounded bg-stone-700/60" />
              <div className="mt-1 truncate text-[8px] font-bold text-stone-800">{card}</div>
              <div className="mt-1 flex justify-between text-[7px] text-stone-700">
                <span>{index + 1}</span>
                <span>{index + 2}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (variant === "panel") {
    return (
      <div className={`${height} overflow-hidden rounded-xl bg-zinc-950 p-4 text-white`}>
        <div className="flex items-center gap-3">
          <div className="flex h-16 w-16 items-center justify-center rounded bg-red-950 text-amber-500">ROMA</div>
          <div className="flex-1">
            <div className="mb-2 flex gap-5 text-lg font-bold"><span>12</span><span>7</span><span>3</span></div>
            <div className="h-3 rounded-full bg-white/10"><div className="h-3 w-3/4 rounded-full bg-lime-500" /></div>
            <div className="mt-4 flex gap-4 text-xs text-white/60"><span>ACTIONS</span><span>⚔</span><span>♜</span><span>✚</span></div>
          </div>
        </div>
      </div>
    );
  }

  if (variant === "turns") {
    return (
      <div className={`${height} overflow-hidden rounded-xl bg-zinc-950 p-5 text-white`}>
        <div className="text-center text-[11px] font-semibold text-white/60">TURN 7 / 20</div>
        <div className="mt-4 flex items-center justify-center gap-5 text-xl text-white/80">
          {[4, 5, 6, 7, 8, 9, 10].map((n) => (
            <span key={n} className={n === 7 ? "flex h-10 w-10 items-center justify-center rounded-full border border-amber-400 text-amber-300" : ""}>{n}</span>
          ))}
        </div>
        <div className="mx-auto mt-4 w-32 rounded bg-sky-900 px-4 py-2 text-center text-xs font-bold">END TURN</div>
      </div>
    );
  }

  return (
    <div className={`${height} overflow-hidden rounded-xl bg-slate-800`}>
      <div className="relative h-full w-full bg-gradient-to-br from-teal-900 via-stone-700 to-lime-700">
        <div className="absolute inset-0 opacity-35" style={{ backgroundImage: "linear-gradient(30deg, transparent 44%, rgba(255,255,255,.65) 45%, rgba(255,255,255,.65) 46%, transparent 47%), linear-gradient(150deg, transparent 44%, rgba(255,255,255,.55) 45%, rgba(255,255,255,.55) 46%, transparent 47%)", backgroundSize: "42px 36px" }} />
        <div className="absolute left-8 top-8 h-8 w-8 rounded-full border-2 border-red-300 bg-red-900/80" />
        <div className="absolute left-28 top-14 h-7 w-7 rounded-full border-2 border-sky-200 bg-sky-900/80" />
        <div className="absolute bottom-7 right-10 h-8 w-8 rounded-full border-2 border-amber-200 bg-amber-900/80" />
        <div className="absolute right-0 top-0 h-full w-20 bg-black/45 p-2 text-[7px] text-white/60">
          <div className="mb-2 h-2 w-12 rounded bg-white/30" />
          <div className="space-y-1.5">{Array.from({ length: 7 }).map((_, i) => <div key={i} className="h-1.5 rounded bg-white/20" />)}</div>
        </div>
      </div>
    </div>
  );
}

function WargameLogo({ compact = false }) {
  if (compact) {
    return (
      <div className="relative flex h-11 w-11 items-center justify-center rounded-2xl bg-violet-700 text-white shadow-sm">
        <Shield size={23} className="absolute opacity-95" />
        <Swords size={15} className="absolute translate-y-[1px] opacity-90" />
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <div className="relative flex h-11 w-11 items-center justify-center rounded-2xl bg-violet-700 text-white shadow-sm">
        <Shield size={23} className="absolute opacity-95" />
        <Swords size={15} className="absolute translate-y-[1px] opacity-90" />
      </div>
      <div>
        <div className="text-lg font-black tracking-[0.2em] text-slate-950">ARENA</div>
        <div className="text-[10px] font-bold tracking-[0.34em] text-slate-400">WARGAME LAB</div>
      </div>
    </div>
  );
}

function TopBar({ query, setQuery, onAdd, onRefresh, onOpenTaxonomy, sidebarOpen, toggleSidebar }) {
  return (
    <header className="flex h-[76px] shrink-0 items-center gap-4 border-b border-slate-200 bg-white px-4 sm:px-6">
      <button
        onClick={toggleSidebar}
        className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 transition hover:bg-slate-50"
        title={sidebarOpen ? "Свернуть меню" : "Открыть меню"}
      >
        {sidebarOpen ? <PanelLeftClose size={19} /> : <Menu size={19} />}
      </button>

      <div className="hidden w-56 shrink-0 md:block">
        <WargameLogo />
      </div>

      <h1 className="hidden min-w-0 flex-1 truncate text-xl font-bold text-slate-950 lg:block">Локальный лаунчер прототипов Arena</h1>

      <div className="relative w-full max-w-md">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={17} />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Поиск проектов..."
          className="h-11 w-full rounded-xl border border-slate-200 bg-white pl-11 pr-16 text-sm outline-none transition placeholder:text-slate-400 focus:border-violet-300 focus:ring-4 focus:ring-violet-50"
        />
        <span className="absolute right-3 top-1/2 -translate-y-1/2 rounded-md border border-slate-200 px-2 py-0.5 text-[10px] font-semibold text-slate-400">Ctrl K</span>
      </div>

      <button onClick={onAdd} className="hidden h-11 shrink-0 items-center gap-2 rounded-xl bg-violet-700 px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-800 md:flex">
        <Plus size={18} /> Добавить проект
      </button>
      <button onClick={onRefresh} className="hidden h-11 shrink-0 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 md:flex">
        <RefreshCw size={17} /> Обновить
      </button>
      <button onClick={onOpenTaxonomy} className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 transition hover:bg-slate-50">
        <Settings size={18} />
      </button>
    </header>
  );
}

function Sidebar({ categories, activeCategory, setActiveCategory, onOpenTaxonomy, projectCounts, sidebarOpen }) {
  const navItems = ["Все проекты", ...categories];

  return (
    <aside
      className={`flex shrink-0 flex-col border-r border-slate-200 bg-white px-3 py-5 transition-all duration-300 ease-in-out ${
        sidebarOpen ? "w-64" : "w-[88px]"
      }`}
    >
      <div className="mb-5 flex justify-center px-1">
        {sidebarOpen ? <WargameLogo /> : <WargameLogo compact />}
      </div>

      <nav className="space-y-2">
        {navItems.map((item, index) => {
          const Icon = iconForCategory(item);
          const active = activeCategory === item;
          return (
            <button
              key={item}
              onClick={() => setActiveCategory(item)}
              title={!sidebarOpen ? item : undefined}
              className={`flex w-full items-center rounded-xl px-3 py-2.5 text-sm transition ${
                sidebarOpen ? "justify-between" : "justify-center"
              } ${active ? "bg-violet-50 text-violet-700" : "text-slate-700 hover:bg-slate-50"} ${
                index === 5 ? "mt-6 border-t border-slate-100 pt-5" : ""
              }`}
            >
              <span className="flex min-w-0 items-center gap-3">
                <Icon size={17} className={active ? "text-violet-700" : "text-slate-500"} />
                {sidebarOpen && <span className="truncate font-medium">{item}</span>}
              </span>
              {sidebarOpen && <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">{projectCounts[item] || 0}</span>}
            </button>
          );
        })}
      </nav>

      <button
        onClick={onOpenTaxonomy}
        title={!sidebarOpen ? "Настроить категории и теги" : undefined}
        className={`mt-4 flex w-full items-center rounded-xl py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50 ${
          sidebarOpen ? "justify-start gap-3 px-3" : "justify-center px-0"
        }`}
      >
        <SlidersHorizontal size={17} className="text-slate-500" />
        {sidebarOpen && "Настроить"}
      </button>

      <div className="mt-auto space-y-3">
        <div className="rounded-xl border border-slate-200 bg-white p-3">
          {sidebarOpen ? (
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
                <div>
                  <div className="text-xs font-semibold text-slate-800">Локальный сервер</div>
                  <div className="text-xs text-slate-500">Работает</div>
                </div>
              </div>
              <ChevronDown size={15} className="text-slate-400" />
            </div>
          ) : (
            <div className="flex items-center justify-center" title="Локальный сервер работает">
              <span className="h-3 w-3 rounded-full bg-emerald-500" />
            </div>
          )}
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-3">
          {sidebarOpen ? (
            <div className="flex items-center justify-between gap-2">
              <div className="flex min-w-0 items-center gap-2">
                <Database size={17} className="shrink-0 text-slate-500" />
                <div className="min-w-0">
                  <div className="text-xs font-semibold text-slate-800">База проектов</div>
                  <div className="truncate text-xs text-slate-500">D:\Arena\Prototypes</div>
                </div>
              </div>
              <MoreHorizontal size={16} className="shrink-0 text-slate-400" />
            </div>
          ) : (
            <div className="flex items-center justify-center" title="База проектов">
              <Database size={17} className="text-slate-500" />
            </div>
          )}
        </div>

        {sidebarOpen && <div className="px-1 text-xs text-slate-500">v1.4.2</div>}
      </div>
    </aside>
  );
}

function CompactTagFilters({ tags, selectedTags, toggleTag, clearTags }) {
  const [expanded, setExpanded] = useState(false);
  if (!tags.length) return null;
  const visible = expanded ? tags : tags.slice(0, 9);

  return (
    <div className="mb-4 rounded-xl border border-slate-200 bg-white px-3 py-2">
      <div className="flex items-center justify-between gap-3">
        <button onClick={() => setExpanded((value) => !value)} className="flex items-center gap-2 text-xs font-semibold text-slate-700">
          <Hash size={15} className="text-slate-500" />
          Теги
          <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] text-slate-500">{selectedTags.length || tags.length}</span>
          <ChevronDown size={14} className={`transition ${expanded ? "rotate-180" : ""}`} />
        </button>
        {selectedTags.length > 0 && <button onClick={clearTags} className="text-xs font-semibold text-violet-700">Сбросить</button>}
      </div>
      {(expanded || selectedTags.length > 0) && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {visible.map((tag) => {
            const active = selectedTags.includes(tag);
            return (
              <button key={tag} onClick={() => toggleTag(tag)} className={`rounded-md px-2 py-1 text-[11px] font-medium transition ${active ? "bg-violet-100 text-violet-700" : "bg-slate-100 text-slate-600 hover:bg-slate-200"}`}>
                {tag}
              </button>
            );
          })}
          {!expanded && tags.length > visible.length && <button onClick={() => setExpanded(true)} className="rounded-md bg-slate-100 px-2 py-1 text-[11px] font-medium text-slate-500">+{tags.length - visible.length}</button>}
        </div>
      )}
    </div>
  );
}

function ProjectCard({ project, selected, onSelect, onStart, onStop, onDelete, onEdit, onTagClick }) {
  return (
    <article onClick={() => onSelect(project.id)} className={`group overflow-hidden rounded-xl border bg-white transition hover:shadow-md ${selected ? "border-violet-500 ring-2 ring-violet-100" : "border-slate-200"}`}>
      <div className="p-3 pb-0">
        <div className="relative">
          <PreviewArt variant={project.preview} large />
          <button className="absolute right-2 top-2 flex h-8 w-8 items-center justify-center rounded-lg bg-white/85 text-amber-400 shadow-sm backdrop-blur">
            <Star size={15} fill={project.favorite ? "currentColor" : "none"} />
          </button>
        </div>
      </div>

      <div className="p-3">
        <div className="mb-1 flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h3 className="truncate text-base font-bold text-slate-950">{project.title}</h3>
            <p className="mt-1 truncate text-sm text-slate-500">{project.description}</p>
          </div>
          <button onClick={(event) => { event.stopPropagation(); onEdit(project); }} className="rounded-lg p-1.5 text-slate-400 opacity-0 transition hover:bg-slate-100 hover:text-slate-700 group-hover:opacity-100">
            <Pencil size={15} />
          </button>
        </div>

        <div className="mt-3 flex flex-wrap gap-1.5">
          {project.tags.slice(0, 3).map((tag) => (
            <button key={tag} onClick={(event) => { event.stopPropagation(); onTagClick(tag); }} className="rounded-md bg-violet-50 px-2 py-1 text-xs font-medium text-violet-700 hover:bg-violet-100">
              {tag}
            </button>
          ))}
        </div>

        <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-2"><span className={`h-2.5 w-2.5 rounded-full ${statusDot(project.status)}`} />{statusLabel(project.status)}</span>
          <span>Порт: {project.port}</span>
        </div>

        <div className="mt-3 grid grid-cols-[1fr_auto_auto_auto] gap-1.5">
          {project.status === "running" || project.status === "starting" ? (
            <button onClick={(event) => { event.stopPropagation(); onStop(project.id); }} className="flex items-center justify-center gap-1.5 rounded-lg border border-rose-200 bg-white px-3 py-2 text-xs font-semibold text-rose-700 hover:bg-rose-50">
              <Square size={14} /> Закрыть
            </button>
          ) : (
            <button onClick={(event) => { event.stopPropagation(); onStart(project.id); }} className="flex items-center justify-center gap-1.5 rounded-lg border border-violet-200 bg-violet-50 px-3 py-2 text-xs font-semibold text-violet-700 hover:bg-violet-100">
              <Play size={14} /> Запустить
            </button>
          )}
          <button className="rounded-lg border border-slate-200 p-2 text-slate-500 hover:bg-slate-50" title="Открыть"><ExternalLink size={14} /></button>
          <button className="rounded-lg border border-slate-200 p-2 text-slate-500 hover:bg-slate-50" title="Папка"><FolderOpen size={14} /></button>
          <button onClick={(event) => { event.stopPropagation(); onDelete(project.id); }} className="rounded-lg border border-slate-200 p-2 text-slate-400 hover:border-rose-200 hover:bg-rose-50 hover:text-rose-700" title="Убрать"><Trash2 size={14} /></button>
        </div>
      </div>
    </article>
  );
}

function DetailPanel({ project, logs, onEdit, onStop }) {
  if (!project) return null;

  return (
    <aside className="hidden w-[430px] shrink-0 border-l border-slate-200 bg-white xl:block">
      <div className="flex h-full flex-col">
        <div className="flex justify-end px-5 py-4">
          <button className="rounded-lg p-2 text-slate-900 hover:bg-slate-100"><X size={18} /></button>
        </div>

        <div className="px-5">
          <PreviewArt variant={project.preview} large />

          <div className="mt-4 flex items-start justify-between gap-4">
            <div className="min-w-0">
              <h2 className="truncate text-xl font-bold text-slate-950">{project.title}</h2>
              <p className="mt-2 text-sm text-slate-500">{project.description}</p>
            </div>
            <span className={`flex shrink-0 items-center gap-2 rounded-lg px-3 py-1.5 text-sm font-medium ${statusStyles(project.status)}`}>
              <span className={`h-2.5 w-2.5 rounded-full ${statusDot(project.status)}`} />
              {statusLabel(project.status)}
            </span>
          </div>

          <div className="mt-6 space-y-4 text-sm">
            <div>
              <div className="mb-2 text-slate-500">Порт</div>
              <div className="flex items-center gap-2">
                <a className="font-medium text-violet-700" href={`http://localhost:${project.port}`}>http://localhost:{project.port}</a>
                <ExternalLink size={15} className="ml-auto text-slate-500" />
                <Copy size={15} className="text-slate-500" />
              </div>
            </div>

            <div>
              <div className="mb-2 text-slate-500">Путь к проекту</div>
              <div className="flex items-center gap-2 rounded-lg bg-slate-50 p-2 font-mono text-xs text-slate-700">
                <span className="min-w-0 flex-1 truncate">{project.path}</span>
                <FolderOpen size={15} className="text-slate-500" />
              </div>
            </div>

            <div>
              <div className="mb-2 text-slate-500">Технологии</div>
              <div className="flex flex-wrap gap-2">
                {technologyChips.map((tech) => (
                  <span key={tech} className="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-700">{tech}</span>
                ))}
              </div>
            </div>

            <div>
              <div className="mb-2 text-slate-500">Описание</div>
              <p className="leading-6 text-slate-700">{project.longDescription || project.description}</p>
              <button className="mt-2 text-sm font-medium text-violet-700">Показать больше <ChevronDown size={14} className="inline" /></button>
            </div>
          </div>
        </div>

        <div className="mt-5 border-t border-slate-200 px-5 pt-4">
          <div className="mb-3 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-900">Последние логи</h3>
            <button className="text-xs font-medium text-slate-500">Очистить</button>
          </div>
          <div className="h-44 overflow-auto rounded-lg bg-zinc-950 p-3 font-mono text-[11px] leading-5 text-slate-300">
            {logs.map((line, index) => <div key={index}>{line}</div>)}
          </div>
        </div>

        <div className="mt-auto flex items-center justify-between gap-3 px-5 py-5">
          <button onClick={() => onStop(project.id)} className="flex items-center gap-2 rounded-lg border border-rose-200 px-4 py-3 text-sm font-semibold text-rose-700 hover:bg-rose-50">
            <Square size={15} /> Закрыть проект
          </button>
          <button onClick={() => onEdit(project)} className="rounded-lg border border-slate-200 p-3 text-slate-700 hover:bg-slate-50"><Pencil size={16} /></button>
          <button className="rounded-lg border border-slate-200 p-3 text-slate-700 hover:bg-slate-50"><MoreHorizontal size={16} /></button>
        </div>
      </div>
    </aside>
  );
}

function ProjectModal({ open, mode, project, categories, onClose, onSave }) {
  const emptyProject = {
    title: "New Arena Prototype",
    description: "Новый локальный прототип для тестирования идеи.",
    longDescription: "Описание нового прототипа.",
    type: categories[0] || "Без категории",
    port: 5180,
    stack: "Vite + React + TS",
    path: "D:\Arena\Prototypes\new-prototype",
    tags: ["Prototype"],
    preview: "map",
  };

  const [form, setForm] = useState(project || emptyProject);
  const [tagsText, setTagsText] = useState((project || emptyProject).tags.join(", "));

  useEffect(() => {
    const next = project || emptyProject;
    setForm(next);
    setTagsText((next.tags || []).join(", "));
  }, [open, project, categories.join("|")]);

  if (!open) return null;

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function submit() {
    onSave({ ...form, title: form.title.trim() || "Untitled Prototype", port: Number(form.port) || 5173, tags: normalizeTags(tagsText) });
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl rounded-2xl bg-white p-6 shadow-2xl">
        <div className="mb-5 flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-950">{mode === "edit" ? "Редактировать прототип" : "Добавить проект"}</h2>
            <p className="mt-1 text-sm text-slate-500">Настрой название, категорию, теги, порт, путь и внешний вид карточки.</p>
          </div>
          <button onClick={onClose} className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"><X size={20} /></button>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <label className="block md:col-span-2"><span className="mb-1.5 block text-sm font-medium text-slate-700">Название</span><input value={form.title} onChange={(e) => update("title", e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /></label>
          <label className="block md:col-span-2"><span className="mb-1.5 block text-sm font-medium text-slate-700">Описание</span><textarea value={form.description} onChange={(e) => update("description", e.target.value)} rows={2} className="w-full resize-none rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /></label>
          <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">Категория</span><select value={form.type} onChange={(e) => update("type", e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50">{categories.map((category) => <option key={category}>{category}</option>)}</select></label>
          <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">Тип превью</span><select value={form.preview} onChange={(e) => update("preview", e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50"><option value="map">Карта</option><option value="dice">Кубики/механика</option><option value="cards">Карты</option><option value="panel">Панель</option><option value="turns">Трекер ходов</option><option value="hex">Гекс-карта</option></select></label>
          <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">Порт</span><input type="number" value={form.port} onChange={(e) => update("port", e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /></label>
          <label className="block"><span className="mb-1.5 block text-sm font-medium text-slate-700">Стек</span><input value={form.stack} onChange={(e) => update("stack", e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /></label>
          <label className="block md:col-span-2"><span className="mb-1.5 block text-sm font-medium text-slate-700">Теги через запятую</span><input value={tagsText} onChange={(e) => setTagsText(e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /></label>
          <label className="block md:col-span-2"><span className="mb-1.5 block text-sm font-medium text-slate-700">Путь к папке</span><input value={form.path} onChange={(e) => update("path", e.target.value)} className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /></label>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button onClick={onClose} className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50">Отмена</button>
          <button onClick={submit} className="flex items-center gap-2 rounded-xl bg-violet-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-violet-800"><Save size={16} /> Сохранить</button>
        </div>
      </div>
    </div>
  );
}

function TaxonomyModal({ open, categories, setCategories, projects, setProjects, onClose }) {
  const [newCategory, setNewCategory] = useState("");
  if (!open) return null;
  const allTags = Array.from(new Set(projects.flatMap((p) => p.tags))).sort((a, b) => a.localeCompare(b));

  function addCategory() {
    const name = newCategory.trim();
    if (!name || categories.some((c) => c.toLowerCase() === name.toLowerCase())) return;
    setCategories((prev) => [...prev, name]);
    setNewCategory("");
  }

  function renameCategory(oldName, newName) {
    const cleaned = newName.trim();
    if (!cleaned) return;
    setCategories((prev) => prev.map((category) => (category === oldName ? cleaned : category)));
    setProjects((prev) => prev.map((project) => (project.type === oldName ? { ...project, type: cleaned } : project)));
  }

  function deleteCategory(name) {
    const fallback = categories.find((category) => category !== name) || "Без категории";
    setCategories((prev) => prev.filter((category) => category !== name));
    setProjects((prev) => prev.map((project) => (project.type === name ? { ...project, type: fallback } : project)));
  }

  function renameTag(oldTag, newTag) {
    const cleaned = newTag.trim();
    if (!cleaned) return;
    setProjects((prev) => prev.map((project) => ({ ...project, tags: Array.from(new Set(project.tags.map((tag) => (tag === oldTag ? cleaned : tag)))) })));
  }

  function deleteTag(tag) {
    setProjects((prev) => prev.map((project) => ({ ...project, tags: project.tags.filter((item) => item !== tag) })));
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div className="max-h-[88vh] w-full max-w-4xl overflow-auto rounded-2xl bg-white p-6 shadow-2xl">
        <div className="mb-5 flex items-start justify-between">
          <div><h2 className="text-xl font-bold text-slate-950">Настройка категорий и тегов</h2><p className="mt-1 text-sm text-slate-500">Категории управляют левым меню, теги — быстрой фильтрацией.</p></div>
          <button onClick={onClose} className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"><X size={20} /></button>
        </div>
        <div className="grid gap-5 lg:grid-cols-2">
          <section className="rounded-2xl border border-slate-200 p-5">
            <h3 className="mb-4 flex items-center gap-2 text-base font-bold text-slate-950"><SlidersHorizontal size={18} /> Категории</h3>
            <div className="mb-4 flex gap-2"><input value={newCategory} onChange={(e) => setNewCategory(e.target.value)} placeholder="Например: Боевые тесты" className="min-w-0 flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-violet-300 focus:ring-4 focus:ring-violet-50" /><button onClick={addCategory} className="rounded-xl bg-violet-700 px-4 py-2 text-sm font-semibold text-white hover:bg-violet-800">Добавить</button></div>
            <div className="space-y-2">{categories.map((category) => <div key={category} className="flex items-center gap-2 rounded-xl bg-slate-50 p-2"><input defaultValue={category} onBlur={(e) => renameCategory(category, e.target.value)} className="min-w-0 flex-1 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-violet-300" /><span className="rounded-full bg-white px-2 py-1 text-xs text-slate-500">{projects.filter((project) => project.type === category).length}</span><button onClick={() => deleteCategory(category)} className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-700"><Trash2 size={16} /></button></div>)}</div>
          </section>
          <section className="rounded-2xl border border-slate-200 p-5">
            <h3 className="mb-4 flex items-center gap-2 text-base font-bold text-slate-950"><Tags size={18} /> Теги</h3>
            <div className="space-y-2">{allTags.map((tag) => <div key={tag} className="flex items-center gap-2 rounded-xl bg-slate-50 p-2"><input defaultValue={tag} onBlur={(e) => renameTag(tag, e.target.value)} className="min-w-0 flex-1 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-violet-300" /><span className="rounded-full bg-white px-2 py-1 text-xs text-slate-500">{projects.filter((project) => project.tags.includes(tag)).length}</span><button onClick={() => deleteTag(tag)} className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-700"><Trash2 size={16} /></button></div>)}</div>
          </section>
        </div>
        <div className="mt-6 flex justify-end"><button onClick={onClose} className="rounded-xl bg-violet-700 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-800">Готово</button></div>
      </div>
    </div>
  );
}

export default function App() {
  const [projects, setProjects] = useState(initialProjects);
  const [categories, setCategories] = useState(initialCategories);
  const [activeCategory, setActiveCategory] = useState("Все проекты");
  const [query, setQuery] = useState("");
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedId, setSelectedId] = useState(initialProjects[0].id);
  const [projectModal, setProjectModal] = useState({ open: false, mode: "add", project: null });
  const [taxonomyOpen, setTaxonomyOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [logs, setLogs] = useState([
    "10:15:02  > npm run dev",
    "10:15:02  > vite",
    "10:15:03  VITE v5.2.11 ready in 362 ms",
    "10:15:03  ➜ Local:   http://localhost:5173/",
    "10:15:03  ➜ Network: use --host to expose",
    "10:15:03  ➜ press h + enter to show help",
    "10:15:08  [plugin:vite:vue] hmr update /src/views/Map.vue",
    "10:15:12  [vite] client page reload src/main.ts",
  ]);

  const allTags = useMemo(() => Array.from(new Set(projects.flatMap((project) => project.tags))).sort((a, b) => a.localeCompare(b)), [projects]);

  const projectCounts = useMemo(() => {
    const counts = { "Все проекты": projects.length };
    for (const category of categories) counts[category] = projects.filter((project) => project.type === category).length;
    return counts;
  }, [projects, categories]);

  const selectedProject = projects.find((project) => project.id === selectedId) || projects[0];

  const filteredProjects = useMemo(() => {
    return projects.filter((project) => {
      const matchesCategory = activeCategory === "Все проекты" || activeCategory === project.type;
      const text = `${project.title} ${project.description} ${project.type} ${project.tags.join(" ")}`.toLowerCase();
      const matchesQuery = text.includes(query.toLowerCase());
      const matchesTags = selectedTags.length === 0 || selectedTags.every((tag) => project.tags.includes(tag));
      return matchesCategory && matchesQuery && matchesTags;
    });
  }, [projects, activeCategory, query, selectedTags]);

  function appendLog(line) {
    setLogs((prev) => [...prev.slice(-14), line]);
  }

  function updateProjectStatus(id, status) {
    setProjects((prev) => prev.map((project) => (project.id === id ? { ...project, status } : project)));
  }

  function startProject(id) {
    const project = projects.find((item) => item.id === id);
    if (!project) return;
    setSelectedId(id);
    updateProjectStatus(id, "starting");
    appendLog(`10:16:01  > cd "${project.path}"`);
    appendLog("10:16:02  > npm run dev");
    appendLog(`10:16:03  ➜ Local:   http://localhost:${project.port}/`);
    window.setTimeout(() => updateProjectStatus(id, "running"), 700);
  }

  function stopProject(id) {
    const project = projects.find((item) => item.id === id);
    if (!project) return;
    setSelectedId(id);
    updateProjectStatus(id, "stopped");
    appendLog(`10:16:21  > stopped ${project.title}`);
  }

  function deleteProject(id) {
    const next = projects.filter((project) => project.id !== id);
    setProjects(next);
    if (selectedId === id) setSelectedId(next[0]?.id || "");
  }

  function openEdit(project) {
    setProjectModal({ open: true, mode: "edit", project });
  }

  function saveProject(payload) {
    if (projectModal.mode === "edit" && projectModal.project) {
      setProjects((prev) => prev.map((project) => (project.id === projectModal.project.id ? { ...project, ...payload, updated: "Только что" } : project)));
      appendLog(`10:16:40  > updated card: ${payload.title}`);
    } else {
      const id = payload.title.toLowerCase().replace(/[^a-z0-9а-яё]+/gi, "-").replace(/^-|-$/g, "") || `prototype-${Date.now()}`;
      const newProject = { id, ...payload, status: "stopped", updated: "Только что", favorite: false };
      setProjects((prev) => [newProject, ...prev]);
      setSelectedId(id);
      appendLog(`10:16:40  > added prototype: ${payload.title}`);
    }
    setProjectModal({ open: false, mode: "add", project: null });
  }

  function toggleTag(tag) {
    setSelectedTags((prev) => (prev.includes(tag) ? prev.filter((item) => item !== tag) : [...prev, tag]));
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-slate-50 text-slate-950">
      <TopBar
        query={query}
        setQuery={setQuery}
        onAdd={() => setProjectModal({ open: true, mode: "add", project: null })}
        onRefresh={() => appendLog("10:16:48  > refreshed prototypes folder scan")}
        onOpenTaxonomy={() => setTaxonomyOpen(true)}
        sidebarOpen={sidebarOpen}
        toggleSidebar={() => setSidebarOpen((prev) => !prev)}
      />

      <div className="flex min-h-0 flex-1">
        <Sidebar
          categories={categories}
          activeCategory={activeCategory}
          setActiveCategory={setActiveCategory}
          onOpenTaxonomy={() => setTaxonomyOpen(true)}
          projectCounts={projectCounts}
          sidebarOpen={sidebarOpen}
        />

        <main className="min-w-0 flex-1 overflow-auto px-5 py-5">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <button className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700">Сортировка: <span className="font-semibold">Недавние</span> <ChevronDown size={14} className="inline" /></button>
              <span className="text-xs text-slate-500">Показано {filteredProjects.length} из {projects.length} проектов</span>
            </div>
            <div className="flex rounded-xl border border-slate-200 bg-white p-1">
              <button className="rounded-lg bg-violet-50 p-2 text-violet-700"><Grid2X2 size={16} /></button>
              <button className="rounded-lg p-2 text-slate-500 hover:bg-slate-50"><List size={16} /></button>
              <button className="rounded-lg p-2 text-slate-500 hover:bg-slate-50"><Columns3 size={16} /></button>
            </div>
          </div>

          <CompactTagFilters tags={allTags} selectedTags={selectedTags} toggleTag={toggleTag} clearTags={() => setSelectedTags([])} />

          <section className="grid grid-cols-1 gap-5 lg:grid-cols-2 2xl:grid-cols-3">
            {filteredProjects.map((project) => (
              <ProjectCard
                key={project.id}
                project={project}
                selected={selectedProject?.id === project.id}
                onSelect={setSelectedId}
                onStart={startProject}
                onStop={stopProject}
                onDelete={deleteProject}
                onEdit={openEdit}
                onTagClick={toggleTag}
              />
            ))}
          </section>

          {filteredProjects.length === 0 && <div className="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center text-slate-500">Ничего не найдено. Попробуй другой поиск, категорию или теги.</div>}
        </main>

        <DetailPanel project={selectedProject} logs={logs} onEdit={openEdit} onStop={stopProject} />
      </div>

      <ProjectModal open={projectModal.open} mode={projectModal.mode} project={projectModal.project} categories={categories} onClose={() => setProjectModal({ open: false, mode: "add", project: null })} onSave={saveProject} />
      <TaxonomyModal open={taxonomyOpen} categories={categories} setCategories={setCategories} projects={projects} setProjects={setProjects} onClose={() => setTaxonomyOpen(false)} />
    </div>
  );
}
