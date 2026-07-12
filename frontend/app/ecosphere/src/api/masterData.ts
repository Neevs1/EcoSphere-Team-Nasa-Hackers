import { apiClient } from '@/lib/client';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// --- Shared Types ---
export interface PaginatedResponse<T> {
  items: T[];
  total: int;
  page: int;
  page_size: int;
  total_pages: int;
}

// --- EsgConfiguration ---
export interface EsgConfiguration {
  id: number;
  auto_emission_calculation: boolean;
  require_evidence_for_csr: boolean;
  environmental_weight: number;
  social_weight: number;
  governance_weight: number;
}

export const useEsgConfiguration = () => {
  return useQuery({
    queryKey: ['esg-configuration'],
    queryFn: () => apiClient.get<EsgConfiguration>('/settings/esg-configuration').then(res => res.data),
  });
};

export const useUpdateEsgConfiguration = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<EsgConfiguration>) => 
      apiClient.patch<EsgConfiguration>('/settings/esg-configuration', data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['esg-configuration'] });
    },
  });
};

// --- Departments ---
export interface Department {
  id: number;
  name: string;
  code: string;
  head_employee_id: number | null;
  parent_department_id: number | null;
  employee_count: number;
  status: boolean;
}

export const useDepartments = (search?: string, page = 1) => {
  return useQuery({
    queryKey: ['departments', search, page],
    queryFn: () => {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      params.append('page', page.toString());
      return apiClient.get<PaginatedResponse<Department>>(`/departments?${params.toString()}`).then(res => res.data);
    },
  });
};

// --- Categories ---
export interface Category {
  id: number;
  name: string;
  type: string;
  status: boolean;
}

export const useCategories = (search?: string, page = 1) => {
  return useQuery({
    queryKey: ['categories', search, page],
    queryFn: () => {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      params.append('page', page.toString());
      return apiClient.get<PaginatedResponse<Category>>(`/categories?${params.toString()}`).then(res => res.data);
    },
  });
};
