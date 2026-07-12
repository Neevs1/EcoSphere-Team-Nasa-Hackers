import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { apiClient, setTokenGetter } from "@/lib/client";

type UserRole =
  | "employee"
  | "department_head"
  | "esg_admin"
  | "compliance_officer"
  | "system_admin";

interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  department_id: number | null;
  points_balance: number;
  xp_total: number;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => {
      // Register token getter with the API client (avoids circular dependency)
      setTokenGetter(() => get().token);

      // Listen for unauthorized events to clear store automatically
      if (typeof window !== "undefined") {
        window.addEventListener("auth:unauthorized", () => {
          set({
            token: null,
            user: null,
            isAuthenticated: false,
            error: "Session expired. Please log in again.",
          });
        });
      }

      return {
    token: null,
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,

    login: async (email: string, password: string) => {
      set({ isLoading: true, error: null });
      try {
        const response = await apiClient.post<LoginResponse>("/auth/login", { email, password });

        set({
          token: response.data.access_token,
          user: response.data.user,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      } catch (err) {
        const message = err instanceof Error ? err.message : "Login failed";
        set({
          token: null,
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: message,
        });
        throw err;
      }
    },

    logout: () => {
      set({
        token: null,
        user: null,
        isAuthenticated: false,
        error: null,
      });
    },

    clearError: () => set({ error: null }),
      };
    },
    {
      name: "ecosphere-auth",
    }
  )
);
