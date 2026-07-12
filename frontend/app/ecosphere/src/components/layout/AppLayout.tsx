import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import {
  LayoutDashboard,
  Leaf,
  Users,
  Shield,
  Trophy,
  FileText,
  Settings,
  Bell,
  Search,
  LogOut,
  ChevronLeft,
} from "lucide-react";
import { useNotificationCount } from "@/api/notifications";

const NAV_ITEMS = [
  { to: "/", icon: LayoutDashboard, label: "Overview" },
  { to: "/environmental", icon: Leaf, label: "Environmental" },
  { to: "/social", icon: Users, label: "Social" },
  { to: "/governance", icon: Shield, label: "Governance" },
  { to: "/gamification", icon: Trophy, label: "Gamification" },
  { to: "/reports", icon: FileText, label: "Reports" },
  { to: "/settings", icon: Settings, label: "Settings" },
];

export function AppLayout() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);
  const { data: unreadData } = useNotificationCount();
  const unreadCount = unreadData?.count ?? 0;

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`flex flex-col border-r border-border bg-card transition-all duration-200 ease-out ${
          collapsed ? "w-[68px]" : "w-[240px]"
        }`}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 h-16 border-b border-border shrink-0">
          <div
            className="flex items-center justify-center w-8 h-8 rounded-lg shrink-0"
            style={{ backgroundColor: "var(--primary)" }}
          >
            <Leaf className="w-4 h-4 text-white" strokeWidth={2} />
          </div>
          {!collapsed && (
            <span className="text-body font-semibold text-foreground">
              EcoSphere
            </span>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-[var(--radius-input)] text-small font-medium transition-all duration-150 ease-out ${
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`
              }
            >
              <item.icon className="w-[18px] h-[18px] shrink-0" strokeWidth={2} />
              {!collapsed && <span>{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* Collapse toggle */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center justify-center h-10 border-t border-border text-muted-foreground hover:text-foreground transition-colors"
        >
          <ChevronLeft
            className={`w-4 h-4 transition-transform duration-200 ${
              collapsed ? "rotate-180" : ""
            }`}
            strokeWidth={2}
          />
        </button>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="flex items-center justify-between h-16 px-8 border-b border-border bg-card shrink-0">
          <div className="flex items-center gap-3 flex-1 max-w-md">
            <div className="flex items-center gap-2 w-full px-3 py-2 rounded-[var(--radius-input)] bg-muted text-muted-foreground">
              <Search className="w-4 h-4 shrink-0" strokeWidth={2} />
              <input
                type="text"
                placeholder="Search anything..."
                className="bg-transparent border-none outline-none text-small flex-1 text-foreground placeholder:text-muted-foreground"
              />
              <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-caption font-medium text-muted-foreground bg-background border border-border rounded">
                ⌘K
              </kbd>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Notifications bell */}
            <button
              onClick={() => navigate("/notifications")}
              className="relative p-2 rounded-[var(--radius-input)] text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
            >
              <Bell className="w-[18px] h-[18px]" strokeWidth={2} />
              {unreadCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 flex items-center justify-center w-4 h-4 text-[10px] font-semibold text-white bg-destructive rounded-full">
                  {unreadCount > 9 ? "9+" : unreadCount}
                </span>
              )}
            </button>

            {/* User */}
            <div className="flex items-center gap-3 pl-3 border-l border-border">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="text-small font-semibold text-primary">
                  {user?.name?.charAt(0) ?? "U"}
                </span>
              </div>
              {user && (
                <div className="hidden sm:block">
                  <p className="text-small font-medium text-foreground leading-tight">
                    {user.name}
                  </p>
                  <p className="text-caption text-muted-foreground capitalize leading-tight">
                    {user.role?.replace("_", " ")}
                  </p>
                </div>
              )}
              <button
                onClick={handleLogout}
                className="p-1.5 rounded-md text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
                title="Logout"
              >
                <LogOut className="w-4 h-4" strokeWidth={2} />
              </button>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
