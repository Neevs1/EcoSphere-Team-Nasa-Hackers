import { useState } from "react";
import { Trophy, Award, Gift, BarChart3 } from "lucide-react";
import { DataTable } from "@/components/ui/DataTable";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useChallenges, useBadges, useRewards, useLeaderboard } from "@/api/domain";

type Tab = "challenges" | "badges" | "rewards" | "leaderboard";

export function GamificationPage() {
  const [tab, setTab] = useState<Tab>("challenges");
  const { data: challenges, isLoading: chLoading } = useChallenges();
  const { data: badges, isLoading: bgLoading } = useBadges();
  const { data: rewards, isLoading: rwLoading } = useRewards();
  const { data: leaderboard, isLoading: lbLoading } = useLeaderboard();

  const tabs: { id: Tab; label: string; icon: typeof Trophy }[] = [
    { id: "challenges", label: "Challenges", icon: Trophy },
    { id: "badges", label: "Badges", icon: Award },
    { id: "rewards", label: "Rewards", icon: Gift },
    { id: "leaderboard", label: "Leaderboard", icon: BarChart3 },
  ];

  return (
    <div className="space-y-8 max-w-[1400px]">
      <div>
        <h1 className="text-h1 font-semibold text-foreground">Gamification</h1>
        <p className="text-body text-muted-foreground mt-1">
          Challenges, badges, rewards, and employee leaderboards.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-muted/50 p-1 rounded-[var(--radius-btn)] w-fit">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-[var(--radius-input)] text-small font-medium transition-all duration-150 ${
              tab === t.id
                ? "bg-card text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <t.icon className="w-4 h-4" strokeWidth={2} />
            {t.label}
          </button>
        ))}
      </div>

      {/* Challenges */}
      {tab === "challenges" && (
        <DataTable
          columns={[
            { key: "id", header: "ID" },
            { key: "title", header: "Title" },
            { key: "xp", header: "XP" },
            { key: "difficulty", header: "Difficulty" },
            { key: "deadline", header: "Deadline" },
            {
              key: "status",
              header: "Status",
              render: (r: any) => <StatusBadge status={r.status ?? "Draft"} />,
            },
          ]}
          data={(challenges as any[]) ?? []}
          isLoading={chLoading}
          emptyMessage="No challenges yet"
        />
      )}

      {/* Badges */}
      {tab === "badges" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {bgLoading && (
            <p className="col-span-full text-center text-muted-foreground py-12">Loading...</p>
          )}
          {badges?.map((badge) => (
            <div
              key={badge.id}
              className="rounded-[var(--radius-card)] border border-border bg-card p-6 hover:shadow-[var(--shadow-hover)] transition-shadow"
            >
              <div className="flex items-center gap-4 mb-3">
                <div className="w-12 h-12 rounded-full bg-[#F59E0B]/10 flex items-center justify-center text-2xl">
                  🏆
                </div>
                <div>
                  <h3 className="text-body font-semibold text-foreground">{badge.name}</h3>
                  <p className="text-caption text-muted-foreground">{badge.description ?? "—"}</p>
                </div>
              </div>
              {badge.unlock_rule && (
                <p className="text-caption text-muted-foreground">
                  Unlock: {(badge.unlock_rule as any)?.metric} ≥ {(badge.unlock_rule as any)?.threshold}
                </p>
              )}
            </div>
          ))}
          {!bgLoading && badges?.length === 0 && (
            <p className="col-span-full text-center text-muted-foreground py-12">No badges yet</p>
          )}
        </div>
      )}

      {/* Rewards */}
      {tab === "rewards" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {rwLoading && (
            <p className="col-span-full text-center text-muted-foreground py-12">Loading...</p>
          )}
          {rewards?.map((reward) => (
            <div
              key={reward.id}
              className="rounded-[var(--radius-card)] border border-border bg-card p-6 hover:shadow-[var(--shadow-hover)] transition-shadow"
            >
              <h3 className="text-body font-semibold text-foreground mb-1">{reward.name}</h3>
              <p className="text-caption text-muted-foreground mb-4">{reward.description ?? "—"}</p>
              <div className="flex items-center justify-between">
                <span className="text-small font-medium text-primary">{reward.points_required} pts</span>
                <span className="text-caption text-muted-foreground">{reward.stock} in stock</span>
              </div>
            </div>
          ))}
          {!rwLoading && rewards?.length === 0 && (
            <p className="col-span-full text-center text-muted-foreground py-12">No rewards yet</p>
          )}
        </div>
      )}

      {/* Leaderboard */}
      {tab === "leaderboard" && (
        <DataTable
          columns={[
            {
              key: "rank",
              header: "#",
              render: (_: any, i?: number) => (
                <span className="font-semibold text-muted-foreground">{(i ?? 0) + 1}</span>
              ),
            },
            { key: "name", header: "Name" },
            { key: "xp_total", header: "XP", render: (r: any) => (
              <span className="font-semibold text-foreground">{r.xp_total}</span>
            )},
            { key: "points_balance", header: "Points" },
          ]}
          data={(leaderboard as any[]) ?? []}
          isLoading={lbLoading}
          emptyMessage="No leaderboard data"
        />
      )}
    </div>
  );
}
