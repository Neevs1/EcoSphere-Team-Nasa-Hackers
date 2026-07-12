import { apiClient } from "@/lib/client";
import { useQuery } from "@tanstack/react-query";

interface NotificationData {
  id: number;
  type: string;
  message: string;
  priority: string;
  related_entity_type: string | null;
  related_entity_id: number | null;
  read_at: string | null;
  created_at: string | null;
}

export const useNotifications = (unread?: boolean) =>
  useQuery({
    queryKey: ["notifications", unread],
    queryFn: () => {
      const params = new URLSearchParams();
      if (unread) params.append("unread", "true");
      return apiClient
        .get<NotificationData[]>(`/notifications?${params}`)
        .then((r) => r.data);
    },
  });

export const useNotificationCount = () =>
  useQuery({
    queryKey: ["notification-count"],
    queryFn: () =>
      apiClient
        .get<{ count: number }>("/notifications/unread-count")
        .then((r) => r.data),
    refetchInterval: 30_000,
  });

export const markNotificationRead = (id: number) =>
  apiClient.patch(`/notifications/${id}/read`);
