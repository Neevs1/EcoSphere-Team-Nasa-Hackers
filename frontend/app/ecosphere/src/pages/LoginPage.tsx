import { useState, type FormEvent } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import { Leaf } from "lucide-react";

/**
 * Login page — wired to POST /api/v1/auth/login.
 * Uses the EcoSphere design system tokens.
 * No signup link — sprint spec says seed-only users.
 */
export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const login = useAuthStore((s) => s.login);
  const isLoading = useAuthStore((s) => s.isLoading);
  const error = useAuthStore((s) => s.error);
  const clearError = useAuthStore((s) => s.clearError);

  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || "/";

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    clearError();

    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch {
      // Error is already set in the store
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-[400px]">
        {/* Logo / Brand */}
        <div className="flex flex-col items-center mb-8">
          <div
            className="flex items-center justify-center w-12 h-12 rounded-[var(--radius-btn)] mb-4"
            style={{ backgroundColor: "var(--primary)" }}
          >
            <Leaf className="w-6 h-6 text-primary-foreground" strokeWidth={2} />
          </div>
          <h1 className="text-h2 font-semibold text-foreground">EcoSphere</h1>
          <p className="text-small text-muted-foreground mt-1">
            ESG Management Platform
          </p>
        </div>

        {/* Login Card */}
        <div
          className="rounded-[var(--radius-card)] border border-border bg-card p-6"
          style={{ boxShadow: "var(--shadow-normal)" }}
        >
          <div className="mb-6">
            <h2 className="text-h4 font-medium text-card-foreground">Sign in</h2>
            <p className="text-small text-muted-foreground mt-1">
              Enter your credentials to access the platform
            </p>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            {/* Error message */}
            {error && (
              <div className="rounded-[var(--radius-input)] border border-destructive/30 bg-destructive/5 px-3 py-2">
                <p className="text-small text-destructive">{error}</p>
              </div>
            )}

            {/* Email field */}
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="email"
                className="text-small font-medium text-foreground"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="admin@ecosphere.dev"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                className="h-10 w-full rounded-[var(--radius-input)] border border-input bg-background px-3 text-body text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent transition-[box-shadow,border-color] duration-150 ease-out"
              />
            </div>

            {/* Password field */}
            <div className="flex flex-col gap-1.5">
              <label
                htmlFor="password"
                className="text-small font-medium text-foreground"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                className="h-10 w-full rounded-[var(--radius-input)] border border-input bg-background px-3 text-body text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent transition-[box-shadow,border-color] duration-150 ease-out"
              />
            </div>

            {/* Submit button */}
            <button
              type="submit"
              disabled={isLoading}
              className="mt-2 h-10 w-full rounded-[var(--radius-btn)] bg-primary text-primary-foreground font-medium text-body transition-all duration-150 ease-out hover:opacity-90 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Signing in…" : "Sign in"}
            </button>
          </form>

          {/* Demo hint */}
          <div className="mt-6 pt-4 border-t border-border">
            <p className="text-caption text-muted-foreground text-center">
              Demo: <span className="font-medium text-foreground">admin@ecosphere.dev</span> / <span className="font-medium text-foreground">admin123</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
