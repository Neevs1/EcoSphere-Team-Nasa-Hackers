import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { Leaf, Users, Shield, Activity } from "lucide-react";
import { ScoreCard } from "@/components/ui/ScoreCard";
import { useDashboardScores } from "@/api/domain";
import { useAuthStore } from "@/store/authStore";

const MOCK_TREND = [
  { month: "Jan", Environmental: 78, Social: 85, Governance: 90 },
  { month: "Feb", Environmental: 80, Social: 86, Governance: 91 },
  { month: "Mar", Environmental: 79, Social: 88, Governance: 89 },
  { month: "Apr", Environmental: 82, Social: 89, Governance: 92 },
  { month: "May", Environmental: 83, Social: 90, Governance: 94 },
  { month: "Jun", Environmental: 84, Social: 92, Governance: 96 },
];

export function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const { data, isLoading } = useDashboardScores();

  const overall = data?.overall_score ?? 0;
  const scores = data?.scores ?? [];

  const topDepts = [...scores]
    .sort((a, b) => b.overall - a.overall)
    .slice(0, 5);

  const envAvg = scores.length
    ? Math.round(scores.reduce((s, d) => s + d.environmental, 0) / scores.length)
    : 0;
  const socAvg = scores.length
    ? Math.round(scores.reduce((s, d) => s + d.social, 0) / scores.length)
    : 0;
  const govAvg = scores.length
    ? Math.round(scores.reduce((s, d) => s + d.governance, 0) / scores.length)
    : 0;

  const greeting = () => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 17) return "Good afternoon";
    return "Good evening";
  };

  return (
    <div className="space-y-8 max-w-[1400px]">
      {/* Header */}
      <div>
        <h1 className="text-h1 font-semibold text-foreground">
          {greeting()}, {user?.name?.split(" ")[0] ?? "User"} 👋
        </h1>
        <p className="text-body text-muted-foreground mt-1">
          Here&apos;s what&apos;s happening with your ESG initiatives today.
        </p>
      </div>

      {/* Score cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <ScoreCard
          title="Overall ESG Score"
          value={Math.round(overall)}
          change={4}
          icon={<Activity className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#10B981"
        />
        <ScoreCard
          title="Environmental Score"
          value={envAvg}
          change={6}
          icon={<Leaf className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#10B981"
        />
        <ScoreCard
          title="Social Score"
          value={socAvg}
          change={3}
          icon={<Users className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#3B82F6"
        />
        <ScoreCard
          title="Governance Score"
          value={govAvg}
          change={8}
          icon={<Shield className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#6366F1"
        />
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Trend chart */}
        <div className="lg:col-span-3 rounded-[var(--radius-card)] border border-border bg-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-h4 font-medium text-foreground">ESG Score Trend</h2>
            <div className="flex gap-2">
              {["6M", "1Y", "All"].map((period) => (
                <button
                  key={period}
                  className="px-3 py-1 text-caption font-medium rounded-md bg-muted text-muted-foreground hover:text-foreground transition-colors"
                >
                  {period}
                </button>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={MOCK_TREND}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
              <XAxis
                dataKey="month"
                tick={{ fontSize: 12, fill: "#6B7280" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 12, fill: "#6B7280" }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  borderRadius: 10,
                  border: "1px solid #E5E7EB",
                  fontSize: 13,
                }}
              />
              <Legend
                iconType="circle"
                iconSize={8}
                wrapperStyle={{ fontSize: 13 }}
              />
              <Line
                type="monotone"
                dataKey="Environmental"
                stroke="#10B981"
                strokeWidth={2.5}
                dot={false}
                activeDot={{ r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="Social"
                stroke="#3B82F6"
                strokeWidth={2.5}
                dot={false}
                activeDot={{ r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="Governance"
                stroke="#6366F1"
                strokeWidth={2.5}
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Department Ranking */}
        <div className="lg:col-span-2 rounded-[var(--radius-card)] border border-border bg-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-h4 font-medium text-foreground">
              Department Ranking
            </h2>
          </div>
          <div className="space-y-0">
            <div className="grid grid-cols-[auto_1fr_auto_auto] gap-x-4 px-2 py-2 text-caption font-medium text-muted-foreground">
              <span>#</span>
              <span>Department</span>
              <span>ESG Score</span>
              <span>Change</span>
            </div>
            {isLoading ? (
              <p className="text-center text-muted-foreground py-8 text-small">
                Loading...
              </p>
            ) : (
              topDepts.map((dept, i) => (
                <div
                  key={dept.department_id}
                  className="grid grid-cols-[auto_1fr_auto_auto] gap-x-4 items-center px-2 py-3 rounded-lg hover:bg-muted/30 transition-colors"
                >
                  <span className="text-small font-medium text-muted-foreground w-6 text-center">
                    {i + 1}
                  </span>
                  <span className="text-small font-medium text-foreground">
                    {dept.department_name}
                  </span>
                  <span className="text-small font-semibold text-foreground tabular-nums">
                    {Math.round(dept.overall)}
                  </span>
                  <span className="text-caption font-medium text-success">
                    ↑ {(Math.random() * 5 + 1).toFixed(0)}%
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
