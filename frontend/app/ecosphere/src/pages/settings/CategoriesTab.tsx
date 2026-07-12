import { useState, useEffect } from 'react';
import { useCategories } from '@/api/masterData';
import { DataTable } from '@/components/ui/DataTable';
import { StatusBadge } from '@/components/ui/StatusBadge';
import { Search, Plus } from 'lucide-react';

export function CategoriesTab() {
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [page, setPage] = useState(1);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchTerm);
      setPage(1);
    }, 500);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  const { data, isLoading } = useCategories(debouncedSearch, page);

  const columns = [
    { key: "name", header: "Name" },
    { key: "description", header: "Description" },
    {
      key: "status",
      header: "Status",
      render: (r: any) => <StatusBadge status={r.status ? "Active" : "Inactive"} />,
    },
    {
      key: "actions",
      header: "",
      align: "right" as const,
      render: () => (
        <div className="flex justify-end gap-3">
          <button className="text-small font-medium text-primary hover:opacity-80 transition-opacity">Edit</button>
          <button className="text-small font-medium text-destructive hover:opacity-80 transition-opacity">Delete</button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-h4 font-medium text-foreground">Categories</h2>
        <div className="flex items-center gap-4">
          <div className="relative flex items-center">
            <Search className="w-4 h-4 text-muted-foreground absolute left-3" />
            <input
              type="text"
              placeholder="Search categories..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 bg-muted border-none rounded-[var(--radius-input)] text-small text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20 w-[240px]"
            />
          </div>
          <button className="flex items-center gap-2 bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-[var(--radius-btn)] text-small font-medium transition-colors">
            <Plus className="w-4 h-4" />
            Add Category
          </button>
        </div>
      </div>

      <DataTable
        columns={columns}
        data={(data?.items as any[]) ?? []}
        isLoading={isLoading}
        emptyMessage="No categories found"
      />

      {data && data.total_pages > 1 && (
        <div className="flex justify-between items-center text-caption text-muted-foreground mt-4 px-2">
          <div>
            Showing <span className="font-medium text-foreground">{((page - 1) * data.page_size) + 1}</span> to <span className="font-medium text-foreground">{Math.min(page * data.page_size, data.total)}</span> of <span className="font-medium text-foreground">{data.total}</span> results
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-3 py-1 bg-muted rounded-md disabled:opacity-50 hover:bg-muted/80 transition-colors text-foreground font-medium"
            >
              Previous
            </button>
            <button
              onClick={() => setPage(p => Math.min(data.total_pages, p + 1))}
              disabled={page === data.total_pages}
              className="px-3 py-1 bg-muted rounded-md disabled:opacity-50 hover:bg-muted/80 transition-colors text-foreground font-medium"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
