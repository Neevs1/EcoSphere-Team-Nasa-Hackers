import { apiClient } from "@/lib/client";
import { useQuery } from "@tanstack/react-query";

// --- Dashboard ---
export interface ScoreData {
  department_id: number;
  department_name: string;
  environmental: number;
  social: number;
  governance: number;
  overall: number;
}

export interface DashboardData {
  scores: ScoreData[];
  overall_score: number;
}

export const useDashboardScores = (departmentId?: number) =>
  useQuery({
    queryKey: ["dashboard-scores", departmentId],
    queryFn: () => {
      const params = new URLSearchParams();
      if (departmentId) params.append("department_id", departmentId.toString());
      return apiClient
        .get<DashboardData>(`/dashboard/scores?${params}`)
        .then((r) => r.data);
    },
  });

// --- Environmental ---
export interface CarbonTransaction {
  id: number;
  department_id: number;
  source_type: string;
  emission_factor_id: number;
  quantity: number;
  co2_calculated: number;
  transaction_date: string;
  created_by: number | null;
}

export const useCarbonTransactions = (departmentId?: number) =>
  useQuery({
    queryKey: ["carbon-transactions", departmentId],
    queryFn: () => {
      const params = new URLSearchParams();
      if (departmentId) params.append("department_id", departmentId.toString());
      return apiClient
        .get<CarbonTransaction[]>(`/carbon-transactions?${params}`)
        .then((r) => r.data);
    },
  });

export const useEnvironmentalDashboard = (departmentId?: number) =>
  useQuery({
    queryKey: ["env-dashboard", departmentId],
    queryFn: () => {
      const params = new URLSearchParams();
      if (departmentId) params.append("department_id", departmentId.toString());
      return apiClient
        .get(`/environmental/dashboard?${params}`)
        .then((r) => r.data);
    },
  });

// --- Social ---
export interface CSRActivity {
  id: number;
  title: string;
  points: number;
  evidence_required: boolean;
  status: string;
  start_date: string | null;
  end_date: string | null;
}

export interface Participation {
  id: number;
  employee_id: number;
  activity_id: number;
  proof_url: string | null;
  approval_status: string;
  points_earned: number;
}

export const useCSRActivities = (status?: string) =>
  useQuery({
    queryKey: ["csr-activities", status],
    queryFn: () => {
      const params = new URLSearchParams();
      if (status) params.append("status", status);
      return apiClient
        .get<CSRActivity[]>(`/csr-activities?${params}`)
        .then((r) => r.data);
    },
  });

export const useParticipations = (status?: string) =>
  useQuery({
    queryKey: ["participations", status],
    queryFn: () => {
      const params = new URLSearchParams();
      if (status) params.append("status", status);
      return apiClient
        .get<Participation[]>(`/participations?${params}`)
        .then((r) => r.data);
    },
  });

export const useSocialDashboard = () =>
  useQuery({
    queryKey: ["social-dashboard"],
    queryFn: () =>
      apiClient.get(`/social/dashboard`).then((r) => r.data),
  });

// --- Governance ---
export interface AuditData {
  id: number;
  title: string;
  department_id: number | null;
  auditor_id: number | null;
  audit_date: string | null;
  findings_summary: string | null;
  status: string;
}

export interface ComplianceIssueData {
  id: number;
  audit_id: number | null;
  severity: string;
  description: string | null;
  owner_id: number;
  department_id: number | null;
  due_date: string;
  status: string;
  is_overdue: boolean;
}

export const useAudits = (departmentId?: number) =>
  useQuery({
    queryKey: ["audits", departmentId],
    queryFn: () => {
      const params = new URLSearchParams();
      if (departmentId) params.append("department_id", departmentId.toString());
      return apiClient
        .get<AuditData[]>(`/audits?${params}`)
        .then((r) => r.data);
    },
  });

export const useComplianceIssues = (filters?: {
  status?: string;
  overdue?: boolean;
}) =>
  useQuery({
    queryKey: ["compliance-issues", filters],
    queryFn: () => {
      const params = new URLSearchParams();
      if (filters?.status) params.append("status", filters.status);
      if (filters?.overdue) params.append("overdue", "true");
      return apiClient
        .get<ComplianceIssueData[]>(`/compliance-issues?${params}`)
        .then((r) => r.data);
    },
  });

// --- Gamification ---
export interface ChallengeData {
  id: number;
  title: string;
  description: string | null;
  xp: number | null;
  difficulty: string | null;
  status: string | null;
  deadline: string | null;
}

export interface BadgeData {
  id: number;
  name: string;
  description: string | null;
  unlock_rule: Record<string, unknown> | null;
  icon_url: string | null;
}

export interface RewardData {
  id: number;
  name: string;
  description: string | null;
  points_required: number;
  stock: number;
}

export interface LeaderboardEntry {
  user_id: number;
  name: string;
  xp_total: number;
  points_balance: number;
  department_id: number | null;
}

export const useChallenges = (status?: string) =>
  useQuery({
    queryKey: ["challenges", status],
    queryFn: () => {
      const params = new URLSearchParams();
      if (status) params.append("status", status);
      return apiClient
        .get<ChallengeData[]>(`/challenges?${params}`)
        .then((r) => r.data);
    },
  });

export const useBadges = () =>
  useQuery({
    queryKey: ["badges"],
    queryFn: () =>
      apiClient.get<BadgeData[]>("/badges").then((r) => r.data),
  });

export const useRewards = () =>
  useQuery({
    queryKey: ["rewards"],
    queryFn: () =>
      apiClient.get<RewardData[]>("/rewards").then((r) => r.data),
  });

export const useLeaderboard = (departmentId?: number) =>
  useQuery({
    queryKey: ["leaderboard", departmentId],
    queryFn: () => {
      const params = new URLSearchParams();
      if (departmentId) params.append("department_id", departmentId.toString());
      return apiClient
        .get<LeaderboardEntry[]>(`/gamification/leaderboard?${params}`)
        .then((r) => r.data);
    },
  });

// --- Reports ---
export interface ReportRow {
  label: string;
  value: number;
  detail: string | null;
}

export const useReport = (
  type: string,
  departmentId?: number,
  dateFrom?: string,
  dateTo?: string
) =>
  useQuery({
    queryKey: ["report", type, departmentId, dateFrom, dateTo],
    queryFn: () => {
      const params = new URLSearchParams();
      if (departmentId)
        params.append("department_id", departmentId.toString());
      if (dateFrom) params.append("date_from", dateFrom);
      if (dateTo) params.append("date_to", dateTo);
      return apiClient
        .get<ReportRow[]>(`/reports/${type}?${params}`)
        .then((r) => r.data);
    },
    enabled: !!type,
  });
