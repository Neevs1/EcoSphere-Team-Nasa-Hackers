import { useState } from 'react';
import { DepartmentsTab } from './DepartmentsTab';
import { CategoriesTab } from './CategoriesTab';
import { EsgConfigurationTab } from './EsgConfigurationTab';
import { Settings as SettingsIcon, Building, Tags, SlidersHorizontal } from 'lucide-react';

type Tab = 'departments' | 'categories' | 'esg';

const TABS: { id: Tab; label: string; icon: typeof SettingsIcon }[] = [
  { id: 'departments', label: 'Departments', icon: Building },
  { id: 'categories', label: 'Categories', icon: Tags },
  { id: 'esg', label: 'ESG Config', icon: SlidersHorizontal },
];

export function SettingsPage() {
  const [activeTab, setActiveTab] = useState<Tab>('departments');

  return (
    <div className="space-y-8 max-w-[1400px]">
      <div>
        <h1 className="text-h1 font-semibold text-foreground">Platform Settings</h1>
        <p className="text-body text-muted-foreground mt-1">
          Manage your master data, categories, and ESG weights.
        </p>
      </div>

      <div className="flex gap-1 bg-muted/50 p-1 rounded-[var(--radius-btn)] w-fit">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-[var(--radius-input)] text-small font-medium transition-all duration-150 ${
              activeTab === t.id
                ? "bg-card text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <t.icon className="w-4 h-4" strokeWidth={2} />
            {t.label}
          </button>
        ))}
      </div>

      <div className="rounded-[var(--radius-card)] border border-border bg-card p-6">
        {activeTab === 'departments' && <DepartmentsTab />}
        {activeTab === 'categories' && <CategoriesTab />}
        {activeTab === 'esg' && <EsgConfigurationTab />}
      </div>
    </div>
  );
}
