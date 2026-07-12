import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

let getToken: (() => string | null) | null = null;

export function setTokenGetter(getter: () => string | null) {
  getToken = getter;
}

apiClient.interceptors.request.use((config) => {
  const token = getToken?.();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.dispatchEvent(new Event("auth:unauthorized"));
    }
    const detail = error.response?.data?.detail || error.message;
    const err = new Error(detail) as Error & { status: number };
    err.status = error.response?.status;
    return Promise.reject(err);
  }
);
