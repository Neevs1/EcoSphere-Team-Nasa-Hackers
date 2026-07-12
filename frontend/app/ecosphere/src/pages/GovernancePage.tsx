import { Shield, AlertTriangle } from "lucide-react";
import { ScoreCard } from "@/components/ui/ScoreCard";
import { DataTable } from "@/components/ui/DataTable";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useAudits, useComplianceIssues } from "@/api/domain";

export function GovernancePage() {
  const { data: audits, isLoading: auditLoading } = useAudits();
  const { data: issues, isLoading: issueLoading } = useComplianceIssues();
  const { data: overdueIssues } = useComplianceIssues({ overdue: true });

  const openCount = issues?.filter((i) => i.status === "Open").length ?? 0;
  const overdueCount = overdueIssues?.length ?? 0;

  return (
    <div className="space-y-8 max-w-[1400px]">
      <div>
        <h1 className="text-h1 font-semibold text-foreground">Governance</h1>
        <p className="text-body text-muted-foreground mt-1">
          Audits, compliance issues, and governance tracking.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <ScoreCard
          title="Total Audits"
          value={audits?.length ?? 0}
          icon={<Shield className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#6366F1"
        />
        <ScoreCard
          title="Open Issues"
          value={openCount}
          icon={<AlertTriangle className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#F59E0B"
        />
        <ScoreCard
          title="Overdue Issues"
          value={overdueCount}
          color="#DC2626"
        />
      </div>

      {/* Audits */}
      <div>
        <h2 className="text-h4 font-medium text-foreground mb-4">Audits</h2>
        <DataTable
          columns={[
            { key: "id", header: "ID" },
            { key: "title", header: "Title" },
            { key: "audit_date", header: "Date" },
            {
              key: "status",
              header: "Status",
              render: (r: any) => <StatusBadge status={r.status} />,
            },
          ]}
          data={(audits as any[]) ?? []}
          isLoading={auditLoading}
          emptyMessage="No audits yet"
        />
      </div>

      {/* Compliance Issues */}
      <div>
        <h2 className="text-h4 font-medium text-foreground mb-4">
          Compliance Issues
        </h2>
        <DataTable
          columns={[
            { key: "id", header: "ID" },
            {
              key: "severity",
              header: "Severity",
              render: (r: any) => <StatusBadge status={r.severity} />,
            },
            { key: "description", header: "Description", render: (r: any) => (
              <span className="max-w-[300px] truncate block">{r.description ?? "—"}</span>
            )},
            { key: "due_date", header: "Due Date" },
            {
              key: "status",
              header: "Status",
              render: (r: any) => (
                <StatusBadge status={r.is_overdue ? "Overdue" : r.status} />
              ),
            },
          ]}
          data={(issues as any[]) ?? []}
          isLoading={issueLoading}
          emptyMessage="No compliance issues"
        />
      </div>
    </div>
  );
}
