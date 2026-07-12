import { useState, useEffect } from 'react';
import { useDepartments } from '@/api/masterData';

export function DepartmentsTab() {
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [page, setPage] = useState(1);

  // Debounce search
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchTerm);
      setPage(1); // Reset page on search
    }, 500);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  const { data, isLoading, isError } = useDepartments(debouncedSearch, page);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold text-slate-100">Departments</h2>
        <div className="flex space-x-4">
          <input
            type="text"
            placeholder="Search departments..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
            Add Department
          </button>
        </div>
      </div>

      <div className="bg-slate-900/50 rounded-lg border border-slate-700/50 overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-800/50 text-slate-400">
            <tr>
              <th className="px-6 py-4 font-medium">Name</th>
              <th className="px-6 py-4 font-medium">Code</th>
              <th className="px-6 py-4 font-medium">Employees</th>
              <th className="px-6 py-4 font-medium">Status</th>
              <th className="px-6 py-4 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {isLoading && (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-slate-400">Loading...</td>
              </tr>
            )}
            {isError && (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-red-400">Failed to load data</td>
              </tr>
            )}
            {data?.items.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-slate-400">No departments found</td>
              </tr>
            )}
            {data?.items.map((dept) => (
              <tr key={dept.id} className="hover:bg-slate-800/30 transition-colors">
                <td className="px-6 py-4 text-slate-200 font-medium">{dept.name}</td>
                <td className="px-6 py-4 text-slate-400">{dept.code}</td>
                <td className="px-6 py-4 text-slate-400">{dept.employee_count}</td>
                <td className="px-6 py-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                    dept.status 
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                      : 'bg-slate-500/10 text-slate-400 border border-slate-500/20'
                  }`}>
                    {dept.status ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 text-right space-x-3">
                  <button className="text-emerald-400 hover:text-emerald-300 transition-colors">Edit</button>
                  <button className="text-red-400 hover:text-red-300 transition-colors">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination controls */}
      {data && data.total_pages > 1 && (
        <div className="flex justify-between items-center text-sm text-slate-400">
          <div>
            Showing <span className="text-slate-200 font-medium">{((page - 1) * data.page_size) + 1}</span> to <span className="text-slate-200 font-medium">{Math.min(page * data.page_size, data.total)}</span> of <span className="text-slate-200 font-medium">{data.total}</span> results
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-3 py-1 bg-slate-800 rounded border border-slate-700 disabled:opacity-50 hover:bg-slate-700 transition-colors"
            >
              Previous
            </button>
            <button
              onClick={() => setPage(p => Math.min(data.total_pages, p + 1))}
              disabled={page === data.total_pages}
              className="px-3 py-1 bg-slate-800 rounded border border-slate-700 disabled:opacity-50 hover:bg-slate-700 transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
