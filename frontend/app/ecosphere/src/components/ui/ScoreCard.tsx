import { type ReactNode } from "react";
import { TrendingUp, TrendingDown } from "lucide-react";

interface ScoreCardProps {
  title: string;
  value: number | string;
  change?: number;
  icon?: ReactNode;
  color?: string;
}

export function ScoreCard({
  title,
  value,
  change,
  icon,
  color = "var(--primary)",
}: ScoreCardProps) {
  const isPositive = (change ?? 0) >= 0;

  return (
    <div
      className="rounded-[var(--radius-card)] border border-border bg-card p-6 transition-shadow duration-200 hover:shadow-[var(--shadow-hover)]"
    >
      <div className="flex items-start justify-between mb-4">
        <p className="text-small font-medium text-muted-foreground">{title}</p>
        {icon && (
          <div
            className="flex items-center justify-center w-9 h-9 rounded-[var(--radius-input)]"
            style={{ backgroundColor: `${color}15` }}
          >
            <span style={{ color }}>{icon}</span>
          </div>
        )}
      </div>
      <p className="text-h1 font-semibold text-foreground tabular-nums">{value}</p>
      {change !== undefined && (
        <div className="flex items-center gap-1 mt-2">
          {isPositive ? (
            <TrendingUp className="w-3.5 h-3.5 text-success" strokeWidth={2} />
          ) : (
            <TrendingDown className="w-3.5 h-3.5 text-destructive" strokeWidth={2} />
          )}
          <span
            className={`text-caption font-medium ${
              isPositive ? "text-success" : "text-destructive"
            }`}
          >
            {isPositive ? "↑" : "↓"} {Math.abs(change)}%
          </span>
          <span className="text-caption text-muted-foreground">vs last month</span>
        </div>
      )}
    </div>
  );
}
