const VARIANTS: Record<string, string> = {
  Active: "bg-[#10B981]/10 text-[#10B981] border-[#10B981]/20",
  Open: "bg-[#3B82F6]/10 text-[#3B82F6] border-[#3B82F6]/20",
  Pending: "bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/20",
  Approved: "bg-[#10B981]/10 text-[#10B981] border-[#10B981]/20",
  Rejected: "bg-[#DC2626]/10 text-[#DC2626] border-[#DC2626]/20",
  Resolved: "bg-[#10B981]/10 text-[#10B981] border-[#10B981]/20",
  "Resolved Late": "bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/20",
  Overdue: "bg-[#DC2626]/10 text-[#DC2626] border-[#DC2626]/20",
  Draft: "bg-gray-100 text-gray-600 border-gray-200",
  Closed: "bg-gray-100 text-gray-500 border-gray-200",
  Completed: "bg-[#6366F1]/10 text-[#6366F1] border-[#6366F1]/20",
  "Under Review": "bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/20",
  Archived: "bg-gray-100 text-gray-500 border-gray-200",
  Critical: "bg-[#DC2626]/10 text-[#DC2626] border-[#DC2626]/20",
  High: "bg-[#F97316]/10 text-[#F97316] border-[#F97316]/20",
  Medium: "bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/20",
  Low: "bg-[#3B82F6]/10 text-[#3B82F6] border-[#3B82F6]/20",
  Inactive: "bg-gray-100 text-gray-500 border-gray-200",
  Informational: "bg-[#3B82F6]/10 text-[#3B82F6] border-[#3B82F6]/20",
  Actionable: "bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/20",
};

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export function StatusBadge({ status, className = "" }: StatusBadgeProps) {
  const variant =
    VARIANTS[status] ?? "bg-gray-100 text-gray-600 border-gray-200";

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-caption font-medium border ${variant} ${className}`}
    >
      {status}
    </span>
  );
}
