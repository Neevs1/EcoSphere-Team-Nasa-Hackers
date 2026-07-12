import { Users, Award, Clock } from "lucide-react";
import { ScoreCard } from "@/components/ui/ScoreCard";
import { DataTable } from "@/components/ui/DataTable";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useCSRActivities, useParticipations, useSocialDashboard } from "@/api/domain";

export function SocialPage() {
  const { data: dashboard } = useSocialDashboard();
  const { data: activities, isLoading: actLoading } = useCSRActivities();
  const { data: participations, isLoading: partLoading } = useParticipations("Pending");

  return (
    <div className="space-y-8 max-w-[1400px]">
      <div>
        <h1 className="text-h1 font-semibold text-foreground">Social</h1>
        <p className="text-body text-muted-foreground mt-1">
          CSR activities, employee participation, and social impact tracking.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-6">
        <ScoreCard
          title="Total Activities"
          value={dashboard?.total_activities ?? 0}
          icon={<Users className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#3B82F6"
        />
        <ScoreCard
          title="Total Participations"
          value={dashboard?.total_participations ?? 0}
          color="#3B82F6"
        />
        <ScoreCard
          title="Pending Approvals"
          value={dashboard?.pending_approvals ?? 0}
          icon={<Clock className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#F59E0B"
        />
        <ScoreCard
          title="Points Awarded"
          value={dashboard?.total_points_awarded ?? 0}
          icon={<Award className="w-[18px] h-[18px]" strokeWidth={2} />}
          color="#10B981"
        />
      </div>

      {/* Activities */}
      <div>
        <h2 className="text-h4 font-medium text-foreground mb-4">CSR Activities</h2>
        <DataTable
          columns={[
            { key: "id", header: "ID" },
            { key: "title", header: "Title" },
            { key: "points", header: "Points" },
            {
              key: "evidence_required",
              header: "Evidence",
              render: (r: any) => r.evidence_required ? "Required" : "Optional",
            },
            {
              key: "status",
              header: "Status",
              render: (r: any) => <StatusBadge status={r.status} />,
            },
          ]}
          data={(activities as any[]) ?? []}
          isLoading={actLoading}
          emptyMessage="No CSR activities yet"
        />
      </div>

      {/* Pending approvals */}
      <div>
        <h2 className="text-h4 font-medium text-foreground mb-4">
          Approval Queue
        </h2>
        <DataTable
          columns={[
            { key: "id", header: "ID" },
            { key: "employee_id", header: "Employee ID" },
            { key: "activity_id", header: "Activity ID" },
            {
              key: "approval_status",
              header: "Status",
              render: (r: any) => <StatusBadge status={r.approval_status} />,
            },
            { key: "points_earned", header: "Points" },
          ]}
          data={(participations as any[]) ?? []}
          isLoading={partLoading}
          emptyMessage="No pending approvals"
        />
      </div>
    </div>
  );
}
