import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LoginPage } from "@/pages/LoginPage";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { AppLayout } from "@/components/layout/AppLayout";

// Pages
import { DashboardPage } from "@/pages/DashboardPage";
import { EnvironmentalPage } from "@/pages/EnvironmentalPage";
import { SocialPage } from "@/pages/SocialPage";
import { GovernancePage } from "@/pages/GovernancePage";
import { GamificationPage } from "@/pages/GamificationPage";
import { ReportsPage } from "@/pages/ReportsPage";
import { SettingsPage } from "@/pages/settings/SettingsPage";
import { NotificationsPage } from "@/pages/NotificationsPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes with layout */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/environmental" element={<EnvironmentalPage />} />
              <Route path="/social" element={<SocialPage />} />
              <Route path="/governance" element={<GovernancePage />} />
              <Route path="/gamification" element={<GamificationPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/notifications" element={<NotificationsPage />} />
            </Route>
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
