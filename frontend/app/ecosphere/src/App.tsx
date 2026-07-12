import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LoginPage } from "@/pages/LoginPage";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { SettingsPage } from "@/pages/settings/SettingsPage";

/**
 * Placeholder page component for authenticated routes.
 * Will be replaced by real module pages in later sprints.
 */
function DashboardPlaceholder() {
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <h1 className="text-h1 font-semibold">Dashboard</h1>
      <p className="text-muted-foreground mt-2">
        Welcome to EcoSphere. Module pages will be built in later sprints.
      </p>
    </div>
  );
}

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

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<DashboardPlaceholder />} />
          {/* Placeholder routes for future sprints */}
          <Route path="/environmental" element={<DashboardPlaceholder />} />
          <Route path="/social" element={<DashboardPlaceholder />} />
          <Route path="/governance" element={<DashboardPlaceholder />} />
          <Route path="/gamification" element={<DashboardPlaceholder />} />
          <Route path="/reports" element={<DashboardPlaceholder />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
  );
}

export default App;
