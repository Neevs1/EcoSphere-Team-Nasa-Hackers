import { useState } from 'react';
import { DepartmentsTab } from './DepartmentsTab';
import { CategoriesTab } from './CategoriesTab';
import { EsgConfigurationTab } from './EsgConfigurationTab';

type Tab = 'departments' | 'categories' | 'esg';

export function SettingsPage() {
  const [activeTab, setActiveTab] = useState<Tab>('departments');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <header>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-500">
            Platform Settings
          </h1>
          <p className="text-slate-400 mt-2 text-lg">
            Manage your master data, categories, and ESG weights.
          </p>
        </header>

        <div className="flex space-x-2 bg-slate-900/50 p-1.5 rounded-xl backdrop-blur-md border border-slate-800/50 w-fit">
          <button
            onClick={() => setActiveTab('departments')}
            className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 ${
              activeTab === 'departments'
                ? 'bg-emerald-500/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            Departments
          </button>
          <button
            onClick={() => setActiveTab('categories')}
            className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 ${
              activeTab === 'categories'
                ? 'bg-emerald-500/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            Categories
          </button>
          <button
            onClick={() => setActiveTab('esg')}
            className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 ${
              activeTab === 'esg'
                ? 'bg-emerald-500/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            ESG Configuration
          </button>
        </div>

        <div className="bg-slate-900/40 rounded-2xl border border-slate-800/50 backdrop-blur-sm p-6 overflow-hidden relative">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-teal-500 opacity-20"></div>
          {activeTab === 'departments' && <DepartmentsTab />}
          {activeTab === 'categories' && <CategoriesTab />}
          {activeTab === 'esg' && <EsgConfigurationTab />}
        </div>
      </div>
    </div>
  );
}
