import { useState } from "react";
import { FileText, Download } from "lucide-react";
import { DataTable } from "@/components/ui/DataTable";
import { useReport } from "@/api/domain";

const REPORT_TYPES = [
  { id: "environmental", label: "Environmental", color: "#10B981" },
  { id: "social", label: "Social", color: "#3B82F6" },
  { id: "governance", label: "Governance", color: "#6366F1" },
  { id: "esg-summary", label: "ESG Summary", color: "#0F766E" },
];

export function ReportsPage() {
  const [selectedReport, setSelectedReport] = useState("esg-summary");
  const { data: reportData, isLoading } = useReport(selectedReport);

  const handleExportCSV = () => {
    if (!reportData || reportData.length === 0) return;

    const headers = "Label,Value,Detail\n";
    const rows = reportData
      .map((r) => `"${r.label}",${r.value},"${r.detail ?? ""}"`)
      .join("\n");
    const csv = headers + rows;
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${selectedReport}-report.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 max-w-[1400px]">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1 font-semibold text-foreground">Reports</h1>
          <p className="text-body text-muted-foreground mt-1">
            Generate and export ESG reports.
          </p>
        </div>
        <button
          onClick={handleExportCSV}
          disabled={!reportData?.length}
          className="flex items-center gap-2 px-4 py-2.5 rounded-[var(--radius-btn)] bg-primary text-white font-medium text-small transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-50"
        >
          <Download className="w-4 h-4" strokeWidth={2} />
          Export CSV
        </button>
      </div>

      {/* Report type selector */}
      <div className="flex gap-4">
        {REPORT_TYPES.map((rt) => (
          <button
            key={rt.id}
            onClick={() => setSelectedReport(rt.id)}
            className={`flex items-center gap-2 px-5 py-3 rounded-[var(--radius-card)] border transition-all duration-150 ${
              selectedReport === rt.id
                ? "border-primary bg-primary/5 text-foreground shadow-sm"
                : "border-border bg-card text-muted-foreground hover:border-primary/30"
            }`}
          >
            <FileText className="w-4 h-4" strokeWidth={2} style={{ color: rt.color }} />
            <span className="text-small font-medium">{rt.label}</span>
          </button>
        ))}
      </div>

      {/* Report data */}
      <DataTable
        columns={[
          { key: "label", header: "Label" },
          {
            key: "value",
            header: "Value",
            render: (r: any) => (
              <span className="font-semibold text-foreground tabular-nums">
                {typeof r.value === "number" ? r.value.toFixed(2) : r.value}
              </span>
            ),
          },
          { key: "detail", header: "Detail" },
        ]}
        data={(reportData as any[]) ?? []}
        isLoading={isLoading}
        emptyMessage="No report data available"
      />
    </div>
  );
}
