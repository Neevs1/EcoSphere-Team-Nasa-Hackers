import { useNotifications, markNotificationRead } from "@/api/notifications";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Bell, Check } from "lucide-react";
import { useQueryClient } from "@tanstack/react-query";

export function NotificationsPage() {
  const { data: notifications, isLoading } = useNotifications();
  const queryClient = useQueryClient();

  const handleMarkRead = async (id: number) => {
    await markNotificationRead(id);
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
    queryClient.invalidateQueries({ queryKey: ["notification-count"] });
  };

  const grouped = {
    Critical: (notifications ?? []).filter((n) => n.priority === "Critical"),
    Actionable: (notifications ?? []).filter((n) => n.priority === "Actionable"),
    Informational: (notifications ?? []).filter((n) => n.priority === "Informational"),
  };

  return (
    <div className="space-y-8 max-w-[800px]">
      <div>
        <h1 className="text-h1 font-semibold text-foreground">Notifications</h1>
        <p className="text-body text-muted-foreground mt-1">
          Stay updated on compliance issues, participations, and achievements.
        </p>
      </div>

      {isLoading && (
        <div className="text-center text-muted-foreground py-12">Loading...</div>
      )}

      {!isLoading && (notifications?.length ?? 0) === 0 && (
        <div className="text-center py-16">
          <Bell className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" strokeWidth={1.5} />
          <p className="text-body text-muted-foreground">No notifications yet</p>
        </div>
      )}

      {Object.entries(grouped).map(
        ([priority, items]) =>
          items.length > 0 && (
            <div key={priority} className="space-y-3">
              <div className="flex items-center gap-2">
                <StatusBadge status={priority} />
                <span className="text-caption text-muted-foreground">
                  ({items.length})
                </span>
              </div>
              <div className="space-y-2">
                {items.map((n) => (
                  <div
                    key={n.id}
                    className={`flex items-start gap-4 p-4 rounded-[var(--radius-card)] border transition-colors ${
                      n.read_at
                        ? "border-border bg-card"
                        : "border-primary/20 bg-primary/[0.02]"
                    }`}
                  >
                    <div className="flex-1 min-w-0">
                      <p className={`text-small ${n.read_at ? "text-muted-foreground" : "text-foreground font-medium"}`}>
                        {n.message}
                      </p>
                      <p className="text-caption text-muted-foreground mt-1">
                        {n.created_at
                          ? new Date(n.created_at).toLocaleString()
                          : ""}
                      </p>
                    </div>
                    {!n.read_at && (
                      <button
                        onClick={() => handleMarkRead(n.id)}
                        className="shrink-0 p-1.5 rounded-md text-muted-foreground hover:text-primary hover:bg-primary/10 transition-colors"
                        title="Mark as read"
                      >
                        <Check className="w-4 h-4" strokeWidth={2} />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )
      )}
    </div>
  );
}
