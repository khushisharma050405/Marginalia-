"use client";
import React, { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

const URL_ = process.env.NEXT_PUBLIC_API_URL || (typeof window !== "undefined" ? "/api_proxy" : "http://127.0.0.1:8000");

export async function api(path: string, opts: any = {}) {
  const t = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const h: any = { ...(opts.headers || {}) };
  if (t) h.Authorization = "Bearer " + t;
  let body = opts.body;
  if (body && !(body instanceof FormData)) {
    h["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  }
  const r = await fetch(URL_ + path, { ...opts, headers: h, body });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) {
    let msg = "Request failed";
    if (typeof j.detail === "string") {
      msg = j.detail;
    } else if (Array.isArray(j.detail)) {
      msg = j.detail
        .map((x: any) => {
          if (typeof x === "string") return x;
          const loc = x.loc && Array.isArray(x.loc) ? x.loc.slice(1).join(".") : "";
          return (loc ? `${loc}: ` : "") + (x.msg || JSON.stringify(x));
        })
        .join("; ");
    } else if (j.detail && typeof j.detail === "object") {
      msg = JSON.stringify(j.detail);
    } else if (j.message) {
      msg = j.message;
    }
    const e: any = new Error(msg);
    e.status = r.status;
    e.data = j;
    throw e;
  }
  return j;
}

export function useApi(path: string) {
  const [d, setD] = useState<any>(null);
  const [err, setErr] = useState("");
  const r = useRouter();

  const load = () =>
    api(path)
      .then(setD)
      .catch((e) => {
        if (e.status === 401) r.push("/login");
        else if (e.status === 409) r.push("/setup");
        else setErr(e.message);
      });

  useEffect(() => {
    load();
    const handleProfileUpdate = () => load();
    window.addEventListener("profile-updated", handleProfileUpdate);
    return () => window.removeEventListener("profile-updated", handleProfileUpdate);
  }, [path]);

  return { d, err, reload: load };
}

const NAV_ITEMS = [
  {
    key: "home",
    label: "Study Home",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
        <polyline points="9 22 9 12 15 12 15 22" />
      </svg>
    ),
  },
  {
    key: "solve",
    label: "Solve",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z" />
      </svg>
    ),
  },
  {
    key: "hub",
    label: "Learning Hub",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <circle cx="12" cy="12" r="3" />
        <line x1="12" y1="2" x2="12" y2="5" />
        <line x1="12" y1="19" x2="12" y2="22" />
        <line x1="2" y1="12" x2="5" y2="12" />
        <line x1="19" y1="12" x2="22" y2="12" />
      </svg>
    ),
  },
  {
    key: "growth",
    label: "Growth",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="20" x2="18" y2="4" />
        <line x1="12" y1="20" x2="12" y2="10" />
        <line x1="6" y1="20" x2="6" y2="16" />
      </svg>
    ),
  },
  {
    key: "notes",
    label: "Study Notes",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
  },
  {
    key: "history",
    label: "History",
    icon: (
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
    ),
  },
];

const FOUNDATION_CLASSES = ["Nursery", "LKG", "UKG"];
const PRIMARY_CLASSES = ["1", "2", "3", "4", "5"];
const MIDDLE_CLASSES = ["6", "7", "8"];
const SECONDARY_CLASSES = ["9", "10"];
const SENIOR_CLASSES = ["11", "12"];
const STREAMS = ["Science", "Commerce", "Humanities"];

interface NotificationItem {
  id: string;
  title: string;
  description: string;
  time: string;
  type: "feature" | "goal" | "update" | "tip";
  link?: string;
  linkText?: string;
}

const DEFAULT_NOTIFICATIONS: NotificationItem[] = [
  {
    id: "notif-diagrams",
    title: "Visual Flowcharts & Diagrams Ready",
    description: "Homework solver now auto-generates interactive Mermaid flowcharts, function graphs, and SVG illustrations with full PNG/SVG export.",
    time: "Just now",
    type: "feature",
    link: "/solve",
    linkText: "Try Solver",
  },
  {
    id: "notif-ocr",
    title: "Attach Images & PDF Question Papers",
    description: "Scan handwritten question sheets or upload textbook PDFs directly to extract and solve questions with verified answers.",
    time: "15m ago",
    type: "feature",
    link: "/solve",
    linkText: "Upload Question",
  },
  {
    id: "notif-streak",
    title: "Daily Practice Goal: 10 Questions",
    description: "Keep your daily study momentum going! Solve questions in your core subjects to maintain your streak.",
    time: "1h ago",
    type: "goal",
    link: "/hub",
    linkText: "Practice Hub",
  },
  {
    id: "notif-curriculum",
    title: "Curriculum & Marking Scheme Active",
    description: "All solutions are aligned with NCERT rationalized syllabus and official board exam step-marking criteria.",
    time: "Today",
    type: "update",
    link: "/home",
    linkText: "View Subjects",
  },
  {
    id: "notif-tip",
    title: "Board Exam Strategy: Steps & Units",
    description: "In numericals, explicitly write Given, Formula, Step-by-step Substitution, and Final Answer with correct SI units for 100% marks.",
    time: "Yesterday",
    type: "tip",
    link: "/notes",
    linkText: "Study Notes",
  },
];

export function Shell({ title, sub, children }: any) {
  const p = usePathname();
  const r = useRouter();
  const [u, setU] = useState<any>(null);

  // Notification State
  const [notifOpen, setNotifOpen] = useState(false);
  const [notifTab, setNotifTab] = useState<"all" | "unread">("all");
  const [readNotifIds, setReadNotifIds] = useState<string[]>([]);
  const [dismissedNotifIds, setDismissedNotifIds] = useState<string[]>([]);
  const notifRef = useRef<HTMLDivElement>(null);

  // Load saved notification read / dismissed states from localStorage
  useEffect(() => {
    try {
      const savedRead = localStorage.getItem("marginalia_notif_read");
      if (savedRead) setReadNotifIds(JSON.parse(savedRead));
      const savedDismissed = localStorage.getItem("marginalia_notif_dismissed");
      if (savedDismissed) setDismissedNotifIds(JSON.parse(savedDismissed));
    } catch (e) {}
  }, []);

  // Handle click outside & escape key to close notifications
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setNotifOpen(false);
      }
    }
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") setNotifOpen(false);
    }
    if (notifOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      document.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [notifOpen]);

  const markAsRead = (id: string) => {
    setReadNotifIds((prev) => {
      if (prev.includes(id)) return prev;
      const next = [...prev, id];
      try {
        localStorage.setItem("marginalia_notif_read", JSON.stringify(next));
      } catch (e) {}
      return next;
    });
  };

  const markAllAsRead = () => {
    const allIds = DEFAULT_NOTIFICATIONS.map((n) => n.id);
    setReadNotifIds(allIds);
    try {
      localStorage.setItem("marginalia_notif_read", JSON.stringify(allIds));
    } catch (e) {}
  };

  const dismissNotification = (id: string) => {
    setDismissedNotifIds((prev) => {
      const next = [...prev, id];
      try {
        localStorage.setItem("marginalia_notif_dismissed", JSON.stringify(next));
      } catch (e) {}
      return next;
    });
  };

  const resetNotifications = () => {
    setReadNotifIds([]);
    setDismissedNotifIds([]);
    try {
      localStorage.removeItem("marginalia_notif_read");
      localStorage.removeItem("marginalia_notif_dismissed");
    } catch (e) {}
  };

  const activeNotifications = DEFAULT_NOTIFICATIONS.filter(
    (n) => !dismissedNotifIds.includes(n.id)
  ).map((n) => ({
    ...n,
    read: readNotifIds.includes(n.id),
  }));

  const unreadCount = activeNotifications.filter((n) => !n.read).length;

  const displayedNotifications = activeNotifications.filter((n) =>
    notifTab === "unread" ? !n.read : true
  );

  const handleNotificationClick = (n: typeof activeNotifications[0]) => {
    markAsRead(n.id);
    if (n.link) {
      setNotifOpen(false);
      r.push(n.link);
    }
  };

  // Class Changer Modal State
  const [classModalOpen, setClassModalOpen] = useState(false);
  const [selBoard, setSelBoard] = useState("CBSE");
  const [selClass, setSelClass] = useState("3");
  const [selStream, setSelStream] = useState<string | null>(null);
  const [savingClass, setSavingClass] = useState(false);
  const [classError, setClassError] = useState("");
  const [toastMessage, setToastMessage] = useState("");

  const loadUser = () => {
    api("/me")
      .then((x) => {
        if (!x.board) r.push("/setup");
        else {
          setU(x);
          setSelBoard(x.board);
          setSelClass(x.class_level);
          setSelStream(x.stream || null);
        }
      })
      .catch((e) => {
        if (e?.status === 401) r.push("/login");
      });
  };

  useEffect(() => {
    loadUser();
  }, []);

  const openClassPicker = () => {
    if (u) {
      setSelBoard(u.board);
      setSelClass(u.class_level);
      setSelStream(u.stream || (["11", "12"].includes(u.class_level) ? "Science" : null));
      setClassError("");
    }
    setClassModalOpen(true);
  };

  const handleSaveClass = async () => {
    const isSenior = selClass === "11" || selClass === "12";
    if (isSenior && !selStream) {
      setClassError("Please select a stream for Senior Secondary.");
      return;
    }

    setSavingClass(true);
    setClassError("");

    try {
      await api("/me/profile", {
        method: "PUT",
        body: {
          board: selBoard,
          class_level: selClass,
          stream: isSenior ? selStream : null,
        },
      });

      const updated = {
        ...(u || {}),
        board: selBoard,
        class_level: selClass,
        stream: isSenior ? selStream : null,
      };
      setU(updated);
      setClassModalOpen(false);

      // Trigger custom event so all open pages (e.g. Dashboard) reload data
      window.dispatchEvent(new Event("profile-updated"));

      setToastMessage(
        `Switched to ${selBoard} · ${
          FOUNDATION_CLASSES.includes(selClass) ? selClass : "Class " + selClass
        }${isSenior && selStream ? " (" + selStream + ")" : ""}`
      );
      setTimeout(() => setToastMessage(""), 4000);
    } catch (err: any) {
      setClassError(err.message || "Failed to update class");
    } finally {
      setSavingClass(false);
    }
  };

  const currentBoard = u?.board || selBoard;
  const currentClass = u?.class_level || selClass;
  const currentStream = u?.stream || selStream;
  const isSeniorSelected = selClass === "11" || selClass === "12";

  return (
    <div className="min-h-screen flex bg-[#F8F6F0] relative text-[#292A28] font-sans selection:bg-[#E1E8DF] selection:text-[#25382B]">
      {/* Top right organic wave gradient art */}
      <div className="absolute top-0 right-0 w-[600px] h-[340px] pointer-events-none overflow-hidden z-0">
        <svg viewBox="0 0 600 340" fill="none" className="w-full h-full opacity-70">
          <path
            d="M80 0C180 70 280 30 420 70C520 100 580 50 600 10V0H80Z"
            fill="#FCEEE2"
          />
          <path
            d="M260 0C360 60 460 40 600 80V0H260Z"
            fill="#F9E2D2"
          />
        </svg>
      </div>

      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-5 right-5 z-50 bg-[#2D4536] text-[#F3F7F2] px-5 py-3 rounded-2xl shadow-xl flex items-center gap-3 text-xs font-medium animate-in fade-in slide-in-from-top-4 duration-200">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Left Sidebar */}
      <aside className="w-64 min-h-screen p-5 bg-[#EFECE6] border-r border-[#E6E1D8] hidden md:flex flex-col justify-between shrink-0 relative z-20 shadow-xs">
        <div>
          {/* Logo & Brand */}
          <div className="flex items-center gap-2.5 mb-7 px-2">
            <svg className="w-6 h-6 text-[#2D4536]" viewBox="0 0 28 28" fill="currentColor">
              <path d="M5 24C6 16 11 8 23 4C23 14 17 21 8 23L5 24Z" opacity="0.95" />
              <path d="M7 23C4 19 4 14 8 10C9 13 9 17 7 23Z" opacity="0.75" />
            </svg>
            <span className="font-serif text-2xl font-medium tracking-tight text-[#2B2925]">
              Marginalia
            </span>
          </div>

          {/* Nav links */}
          <nav className="space-y-1">
            {NAV_ITEMS.map((item) => {
              const active = p === "/" + item.key || (item.key === "home" && p === "/");
              return (
                <Link
                  key={item.key}
                  href={"/" + item.key}
                  className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all duration-150 ${
                    active
                      ? "bg-[#DFE7DD] text-[#25382B] shadow-xs"
                      : "text-[#554E46] hover:text-[#25221E] hover:bg-[#E7E2D9]"
                  }`}
                >
                  <span className={`${active ? "text-[#25382B]" : "text-[#7A7268]"}`}>
                    {item.icon}
                  </span>
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Log out */}
          <div className="pt-2 px-1">
            <button
              onClick={() => {
                localStorage.removeItem("token");
                r.push("/login");
              }}
              className="flex items-center gap-3 px-2.5 py-2 text-xs font-medium text-[#6B6359] hover:text-[#9B5646] transition-colors rounded-xl"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
              <span>Log out</span>
            </button>
          </div>
        </div>

        {/* Sidebar Footer with Botanical Quote */}
        <div className="pt-8 pb-3 px-2 relative">
          <div className="mb-2">
            <svg className="w-7 h-7 text-[#465A46]/60 -rotate-6" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M6 26C10 21 16 14 26 6" />
              <path d="M12 18C10 14 12 11 16 10C17 14 15 17 12 18Z" fill="currentColor" fillOpacity="0.4" />
              <path d="M18 12C17 8 20 5 24 5C24 9 22 12 18 12Z" fill="currentColor" fillOpacity="0.4" />
              <path d="M10 24C6 22 6 18 9 17C12 19 12 22 10 24Z" fill="currentColor" fillOpacity="0.4" />
            </svg>
          </div>
          <p className="font-serif italic text-xs text-[#524B43] leading-relaxed">
            &ldquo;Small steps<br />build big<br />progress.&rdquo;
          </p>
          <div className="w-8 h-[2px] bg-[#C5BBB0] mt-3 rounded-full" />
        </div>
      </aside>

      {/* Main Workspace (Harmonious full width without gaping empty margins) */}
      <main className="flex-1 px-4 sm:px-8 lg:px-10 py-6 w-full max-w-7xl mx-auto relative z-10 flex flex-col gap-6">
        <div>
          {/* Top Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-7">
            <div>
              <h1 className="font-serif text-3xl md:text-4xl text-[#1E2B22] font-medium tracking-tight">
                {title}
              </h1>
              <p className="text-[#6B6359] text-xs md:text-sm mt-1">{sub}</p>
            </div>

            <div className="flex items-center gap-3 self-end sm:self-center">
              {/* Clickable Class & Board Changer Button (Always available, with reactive fallback) */}
              <button
                type="button"
                onClick={openClassPicker}
                className="group flex items-center gap-2 text-xs font-medium px-4 py-2 rounded-full border border-[#DCD5C9] bg-white/90 hover:bg-white text-[#4A433B] hover:border-[#684D43] shadow-xs hover:shadow-sm transition-all cursor-pointer"
                title="Click to switch your Class, Board, or Stream"
              >
                <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0 animate-pulse" />
                <span className="font-semibold text-[#29221C]">{currentBoard}</span>
                <span className="text-[#8C8377]">·</span>
                <span>
                  {FOUNDATION_CLASSES.includes(currentClass)
                    ? currentClass
                    : `Class ${currentClass}`}
                </span>
                {currentStream && (
                  <>
                    <span className="text-[#8C8377]">·</span>
                    <span className="text-[#684D43] font-medium">{currentStream}</span>
                  </>
                )}
                {/* Subtle Downward Chevron indicating changeability */}
                <svg
                  className="w-3.5 h-3.5 text-[#8C8377] group-hover:text-[#29221C] transition-transform group-hover:translate-y-0.5 ml-0.5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="m6 9 6 6 6-6" />
                </svg>
              </button>

              {/* Notification Interactive Dropdown */}
              <div className="relative" ref={notifRef}>
                <button
                  type="button"
                  onClick={() => setNotifOpen((prev) => !prev)}
                  className={`w-9 h-9 rounded-full border border-[#DCD5C9] flex items-center justify-center text-[#554D45] hover:bg-white shadow-xs relative transition-all cursor-pointer ${
                    notifOpen
                      ? "bg-white ring-2 ring-[#684D43]/20 border-[#684D43]"
                      : "bg-white/80"
                  }`}
                  title={unreadCount > 0 ? `${unreadCount} unread notification${unreadCount > 1 ? "s" : ""}` : "Notifications"}
                  aria-label="Toggle notifications"
                  id="notifications-bell-btn"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
                    <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
                  </svg>
                  {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 rounded-full bg-[#D4784B] text-white text-[10px] font-bold flex items-center justify-center ring-2 ring-[#FAF8F5] shadow-xs">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {/* Notifications Panel */}
                {notifOpen && (
                  <div
                    id="notifications-dropdown-menu"
                    className="absolute right-0 top-12 w-[340px] sm:w-[410px] max-w-[calc(100vw-2rem)] bg-[#FAF8F5] border border-[#E5DFD5] rounded-3xl shadow-2xl p-4 sm:p-5 z-50 animate-in fade-in zoom-in-95 duration-150"
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between pb-3 border-b border-[#EAE3D8]">
                      <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-full bg-[#EAE3D8] flex items-center justify-center text-[#4A433B]">
                          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
                            <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
                          </svg>
                        </div>
                        <div>
                          <h3 className="text-sm font-semibold text-[#29221C]">Notifications</h3>
                          <p className="text-[11px] text-[#7A7369]">
                            {unreadCount > 0 ? `${unreadCount} unread update${unreadCount > 1 ? "s" : ""}` : "All caught up"}
                          </p>
                        </div>
                      </div>

                      {unreadCount > 0 && (
                        <button
                          type="button"
                          onClick={markAllAsRead}
                          className="text-[11px] font-medium text-[#5C463D] hover:text-[#29221C] hover:underline px-2.5 py-1 rounded-lg hover:bg-[#EFECE6] transition-colors"
                        >
                          Mark all as read
                        </button>
                      )}
                    </div>

                    {/* Filter Tabs */}
                    <div className="flex items-center gap-2 pt-3 pb-2">
                      <button
                        type="button"
                        onClick={() => setNotifTab("all")}
                        className={`text-xs px-3 py-1 rounded-full transition-colors font-medium ${
                          notifTab === "all"
                            ? "bg-[#5C463D] text-[#F9F6F0]"
                            : "text-[#6B6359] hover:bg-[#EFECE6]"
                        }`}
                      >
                        All ({activeNotifications.length})
                      </button>
                      <button
                        type="button"
                        onClick={() => setNotifTab("unread")}
                        className={`text-xs px-3 py-1 rounded-full transition-colors font-medium flex items-center gap-1.5 ${
                          notifTab === "unread"
                            ? "bg-[#5C463D] text-[#F9F6F0]"
                            : "text-[#6B6359] hover:bg-[#EFECE6]"
                        }`}
                      >
                        <span>Unread</span>
                        {unreadCount > 0 && (
                          <span
                            className={`text-[10px] px-1.5 py-0.2 rounded-full font-bold ${
                              notifTab === "unread" ? "bg-white/20 text-white" : "bg-[#D4784B] text-white"
                            }`}
                          >
                            {unreadCount}
                          </span>
                        )}
                      </button>
                    </div>

                    {/* Notification items list */}
                    <div className="mt-2 space-y-2 max-h-[380px] overflow-y-auto pr-1">
                      {displayedNotifications.length === 0 ? (
                        <div className="py-8 text-center px-4">
                          <div className="w-10 h-10 rounded-full bg-[#EFECE6] mx-auto flex items-center justify-center text-[#7A7369] mb-2">
                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                              <polyline points="22 4 12 14.01 9 11.01" />
                            </svg>
                          </div>
                          <p className="text-xs font-semibold text-[#29221C]">You're all caught up!</p>
                          <p className="text-[11px] text-[#7A7369] mt-0.5">
                            {notifTab === "unread" ? "No unread notifications left." : "No notifications right now."}
                          </p>
                          <button
                            type="button"
                            onClick={resetNotifications}
                            className="mt-3 text-[11px] text-[#5C463D] hover:underline font-medium inline-block"
                          >
                            Reset notification demo
                          </button>
                        </div>
                      ) : (
                        displayedNotifications.map((n) => (
                          <div
                            key={n.id}
                            onClick={() => handleNotificationClick(n)}
                            className={`group p-3 rounded-2xl border transition-all cursor-pointer relative flex gap-3 ${
                              n.read
                                ? "bg-white/60 hover:bg-white border-[#E8E2D8] text-[#554D45]"
                                : "bg-[#FDFBF7] hover:bg-white border-[#DCD3C5] shadow-xs"
                            }`}
                          >
                            {/* Icon per type */}
                            <div className="shrink-0 mt-0.5">
                              {n.type === "feature" && (
                                <div className="w-8 h-8 rounded-xl bg-[#F6ECE4] text-[#D4784B] flex items-center justify-center border border-[#EDDEC6]">
                                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z" />
                                  </svg>
                                </div>
                              )}
                              {n.type === "goal" && (
                                <div className="w-8 h-8 rounded-xl bg-[#E6EFE6] text-[#2D5A3A] flex items-center justify-center border border-[#CFE0CF]">
                                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <circle cx="12" cy="12" r="10" />
                                    <circle cx="12" cy="12" r="6" />
                                    <circle cx="12" cy="12" r="2" />
                                  </svg>
                                </div>
                              )}
                              {n.type === "update" && (
                                <div className="w-8 h-8 rounded-xl bg-[#EBF0F7] text-[#365A84] flex items-center justify-center border border-[#D1DFEE]">
                                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z" />
                                    <path d="M6 6h10" />
                                    <path d="M6 10h10" />
                                  </svg>
                                </div>
                              )}
                              {n.type === "tip" && (
                                <div className="w-8 h-8 rounded-xl bg-[#F7EFE9] text-[#7A5643] flex items-center justify-center border border-[#E9DCD1]">
                                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M9 18h6" />
                                    <path d="M10 22h4" />
                                    <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14" />
                                  </svg>
                                </div>
                              )}
                            </div>

                            {/* Content */}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-start justify-between gap-1">
                                <h4 className={`text-xs font-semibold leading-snug ${n.read ? "text-[#4A433B]" : "text-[#1E2B22]"}`}>
                                  {n.title}
                                </h4>
                                <span className="text-[10px] text-[#8C8377] shrink-0 whitespace-nowrap ml-1">{n.time}</span>
                              </div>
                              <p className="text-[11px] text-[#6B6359] mt-1 leading-relaxed">
                                {n.description}
                              </p>
                              {n.link && (
                                <div className="mt-2 flex items-center gap-1 text-[11px] font-medium text-[#5C463D] group-hover:text-[#2D4536]">
                                  <span>{n.linkText || "View details"}</span>
                                  <svg className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M5 12h14" />
                                    <path d="m12 5 7 7-7 7" />
                                  </svg>
                                </div>
                              )}
                            </div>

                            {/* Read indicator & Dismiss action */}
                            <div className="flex flex-col items-end justify-between shrink-0 pl-1">
                              {!n.read ? (
                                <span className="w-2 h-2 rounded-full bg-[#D4784B]" title="Unread" />
                              ) : (
                                <div className="w-2 h-2" />
                              )}
                              <button
                                type="button"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  dismissNotification(n.id);
                                }}
                                title="Dismiss notification"
                                className="opacity-0 group-hover:opacity-100 hover:text-[#9B5646] text-[#A0988E] transition-opacity p-1 rounded-md"
                              >
                                <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <line x1="18" y1="6" x2="6" y2="18" />
                                  <line x1="6" y1="6" x2="18" y2="18" />
                                </svg>
                              </button>
                            </div>
                          </div>
                        ))
                      )}
                    </div>

                    {/* Footer */}
                    <div className="mt-3 pt-3 border-t border-[#EAE3D8] flex items-center justify-between text-[11px] text-[#7A7369]">
                      <div className="flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                        <span>Curriculum synced</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => {
                          setNotifOpen(false);
                          r.push("/solve");
                        }}
                        className="text-[#5C463D] font-medium hover:underline flex items-center gap-1"
                      >
                        <span>Open Solver</span>
                        <span>&rarr;</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* User Avatar */}
              <div className="relative">
                <div className="w-9 h-9 rounded-full bg-[#D4937D] text-white font-medium flex items-center justify-center text-sm shadow-xs font-serif">
                  {u?.name ? u.name[0].toUpperCase() : "K"}
                </div>
                <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-[#A88362] border-2 border-[#F8F6F0]" />
              </div>
            </div>
          </div>

          {/* Page Content: Renders directly and reliably */}
          {children}
        </div>

        {/* Footer info tag */}
        <p className="mt-12 text-xs text-[#7D766D] flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block shrink-0" />
          Official CBSE &amp; ICSE Curriculum • Aligned with current NCERT &amp; CISCE academic session
        </p>
      </main>

      {/* Class & Board Switcher Interactive Modal */}
      {classModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
          <div className="bg-[#FAF7F2] border border-[#E5DFD5] w-full max-w-xl rounded-3xl p-6 sm:p-8 shadow-2xl relative animate-in fade-in zoom-in-95 duration-200 max-h-[90vh] overflow-y-auto">
            {/* Close Button */}
            <button
              onClick={() => setClassModalOpen(false)}
              className="absolute top-5 right-5 text-[#8C8377] hover:text-[#25221E] w-8 h-8 rounded-full flex items-center justify-center hover:bg-[#EFECE6] transition-colors"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>

            {/* Modal Header */}
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-full bg-[#E5EDE3] text-[#3D6649] flex items-center justify-center shadow-xs">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z" />
                  <path d="M6 2v20" />
                </svg>
              </div>
              <div>
                <h3 className="font-serif text-xl font-medium text-[#29221C]">
                  Switch Curriculum &amp; Class
                </h3>
                <p className="text-xs text-[#7A7369]">
                  Pick your education board and grade. Your study topics, chapters, and questions will adapt instantly.
                </p>
              </div>
            </div>

            {/* Board Selector */}
            <div className="space-y-2 mb-6">
              <label className="block text-xs font-semibold uppercase tracking-wider text-[#6B6359]">
                1. Education Board
              </label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { id: "CBSE", name: "CBSE", desc: "Central Board (NCERT)" },
                  { id: "ICSE", name: "ICSE", desc: "CISCE Curriculum" },
                ].map((board) => {
                  const active = selBoard === board.id;
                  return (
                    <button
                      key={board.id}
                      type="button"
                      onClick={() => setSelBoard(board.id)}
                      className={`text-left p-3.5 rounded-2xl border transition-all cursor-pointer ${
                        active
                          ? "bg-white border-[#5C463D] ring-2 ring-[#5C463D]/20 shadow-xs"
                          : "bg-[#F3EFE9] border-[#E2D8CC] hover:bg-white text-[#524B43]"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-serif font-medium text-[#2E2420] text-base">
                          {board.name}
                        </span>
                        {active && (
                          <span className="w-4 h-4 rounded-full bg-[#5C463D] text-white flex items-center justify-center text-[10px]">
                            ✓
                          </span>
                        )}
                      </div>
                      <p className="text-[11px] text-[#7A6E65] mt-0.5">{board.desc}</p>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Class Selector */}
            <div className="space-y-3 mb-6">
              <label className="block text-xs font-semibold uppercase tracking-wider text-[#6B6359]">
                2. Select Grade / Class
              </label>

              {/* Foundation */}
              <div>
                <span className="text-[11px] font-medium text-[#8A7F73] block mb-1.5">
                  Early Years
                </span>
                <div className="flex flex-wrap gap-2">
                  {FOUNDATION_CLASSES.map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => {
                        setSelClass(lvl);
                        setSelStream(null);
                      }}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                        selClass === lvl
                          ? "bg-[#5C463D] text-white border-[#5C463D] shadow-xs"
                          : "bg-white text-[#4A433B] border-[#DCD5C9] hover:bg-[#F3EFE9]"
                      }`}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>

              {/* Primary */}
              <div>
                <span className="text-[11px] font-medium text-[#8A7F73] block mb-1.5">
                  Primary School (Classes 1 - 5)
                </span>
                <div className="flex flex-wrap gap-2">
                  {PRIMARY_CLASSES.map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => {
                        setSelClass(lvl);
                        setSelStream(null);
                      }}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                        selClass === lvl
                          ? "bg-[#5C463D] text-white border-[#5C463D] shadow-xs"
                          : "bg-white text-[#4A433B] border-[#DCD5C9] hover:bg-[#F3EFE9]"
                      }`}
                    >
                      Class {lvl}
                    </button>
                  ))}
                </div>
              </div>

              {/* Middle */}
              <div>
                <span className="text-[11px] font-medium text-[#8A7F73] block mb-1.5">
                  Middle &amp; Secondary (Classes 6 - 10)
                </span>
                <div className="flex flex-wrap gap-2">
                  {[...MIDDLE_CLASSES, ...SECONDARY_CLASSES].map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => {
                        setSelClass(lvl);
                        setSelStream(null);
                      }}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                        selClass === lvl
                          ? "bg-[#5C463D] text-white border-[#5C463D] shadow-xs"
                          : "bg-white text-[#4A433B] border-[#DCD5C9] hover:bg-[#F3EFE9]"
                      }`}
                    >
                      Class {lvl}
                    </button>
                  ))}
                </div>
              </div>

              {/* Senior */}
              <div>
                <span className="text-[11px] font-medium text-[#8A7F73] block mb-1.5">
                  Senior Secondary (Classes 11 - 12)
                </span>
                <div className="flex flex-wrap gap-2">
                  {SENIOR_CLASSES.map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => {
                        setSelClass(lvl);
                        if (!selStream) setSelStream("Science");
                      }}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-medium border transition-all cursor-pointer ${
                        selClass === lvl
                          ? "bg-[#5C463D] text-white border-[#5C463D] shadow-xs"
                          : "bg-white text-[#4A433B] border-[#DCD5C9] hover:bg-[#F3EFE9]"
                      }`}
                    >
                      Class {lvl}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Stream Selector (If Class 11 or 12) */}
            {isSeniorSelected && (
              <div className="space-y-2 mb-6 animate-in fade-in duration-150">
                <label className="block text-xs font-semibold uppercase tracking-wider text-[#6B6359]">
                  3. Academic Stream
                </label>
                <div className="grid grid-cols-3 gap-2.5">
                  {STREAMS.map((st) => {
                    const active = selStream === st;
                    return (
                      <button
                        key={st}
                        type="button"
                        onClick={() => setSelStream(st)}
                        className={`p-3 rounded-2xl border text-center transition-all cursor-pointer ${
                          active
                            ? "bg-white border-[#5C463D] ring-2 ring-[#5C463D]/20 shadow-xs"
                            : "bg-[#F3EFE9] border-[#E2D8CC] text-[#4A433B] hover:bg-white"
                        }`}
                      >
                        <span className="text-xs font-serif font-medium block">
                          {st}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {classError && (
              <div className="mb-4 p-3 rounded-xl text-xs bg-[#FBF1EE] border border-[#F0D1C7] text-[#9B6256]">
                {classError}
              </div>
            )}

            {/* Modal Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-[#EAE3D8]">
              <span className="text-xs text-[#7A7369]">
                Selected:{" "}
                <strong className="text-[#29221C]">
                  {selBoard} ·{" "}
                  {FOUNDATION_CLASSES.includes(selClass)
                    ? selClass
                    : `Class ${selClass}`}
                  {isSeniorSelected && selStream ? ` · ${selStream}` : ""}
                </strong>
              </span>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setClassModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-xs font-medium text-[#6B6359] hover:bg-[#EFECE6] transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  disabled={savingClass}
                  onClick={handleSaveClass}
                  className="px-5 py-2.5 rounded-xl bg-[#5C463D] hover:bg-[#483730] text-[#F9F6F0] text-xs font-medium transition-all shadow-xs disabled:opacity-50 flex items-center gap-2"
                >
                  {savingClass && (
                    <svg className="animate-spin h-3.5 w-3.5 text-white" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                  )}
                  <span>{savingClass ? "Updating..." : "Save & Switch"}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
