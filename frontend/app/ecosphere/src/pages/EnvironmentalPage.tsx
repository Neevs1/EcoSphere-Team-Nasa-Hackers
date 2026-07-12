import { Leaf, TrendingDown } from "lucide-react";
import { ScoreCard } from "@/components/ui/ScoreCard";
import { DataTable } from "@/components/ui/DataTable";
import {
  useCarbonTransactions,
  useEnvironmentalDashboard,
} from "@/api/domain";

export function EnvironmentalPage() {
  const { data: dashboard } =
    useEnvironmentalDashboard();
  const { data: transactions, isLoading: txnLoading } =
    useCarbonTransactions();

  return (
    <div className="space-y-8 max-w-[1400px]">
      <div>
        <h1 className="text-h1 font-semibold text-foreground">Environmental</h1>
        <p className="text-body text-muted-foreground mt-1">
          Track carbon emissions, environmental goals, and sustainability metrics.
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <ScoreCard
          title="Total CO₂ Emissions"
          value={`${(dashboard?.total_emissions ?? 0).toFixed(1)} t`}
          icon={<Leaf className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#10B981"
        />
        <ScoreCard
          title="Transactions"
          value={dashboard?.total_transactions ?? 0}
          icon={<TrendingDown className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#0F766E"
        />
        <ScoreCard
          title="Active Goals"
          value={dashboard?.goals?.length ?? 0}
          color="#10B981"
        />
      </div>

      {/* Goals */}
      {dashboard?.goals && dashboard.goals.length > 0 && (
        <div className="rounded-[var(--radius-card)] border border-border bg-card p-6">
          <h2 className="text-h4 font-medium text-foreground mb-4">
            Environmental Goals
          </h2>
          <div className="space-y-4">
            {dashboard.goals.map((goal: any) => {
              const pct = goal.target_co2
                ? Math.min(100, ((goal.current_co2 || 0) / goal.target_co2) * 100)
                : 0;
              return (
                <div key={goal.id} className="space-y-2">
                  <div className="flex justify-between text-small">
                    <span className="font-medium text-foreground">{goal.name}</span>
                    <span className="text-muted-foreground">
                      {(goal.current_co2 ?? 0).toFixed(1)} / {(goal.target_co2 ?? 0).toFixed(1)} t CO₂
                    </span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${pct}%`,
                        backgroundColor: pct > 90 ? "#DC2626" : pct > 70 ? "#F59E0B" : "#10B981",
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Transactions table */}
      <div>
        <h2 className="text-h4 font-medium text-foreground mb-4">
          Carbon Transactions
        </h2>
        <DataTable
          columns={[
            { key: "id", header: "ID" },
            { key: "source_type", header: "Source" },
            { key: "quantity", header: "Quantity", render: (r: any) => r.quantity?.toFixed(2) },
            {
              key: "co2_calculated",
              header: "CO₂ (t)",
              render: (r: any) => (
                <span className={r.co2_calculated < 0 ? "text-success font-medium" : ""}>
                  {r.co2_calculated?.toFixed(4)}
                </span>
              ),
            },
            { key: "transaction_date", header: "Date" },
          ]}
          data={(transactions as any[]) ?? []}
          isLoading={txnLoading}
          emptyMessage="No carbon transactions yet"
        />
      </div>
    </div>
  );
}
