import { useState, useEffect } from 'react';
import { useEsgConfiguration, useUpdateEsgConfiguration } from '@/api/masterData';

export function EsgConfigurationTab() {
  const { data: config, isLoading } = useEsgConfiguration();
  const updateConfig = useUpdateEsgConfiguration();
  
  const [formData, setFormData] = useState({
    auto_emission_calculation: false,
    require_evidence_for_csr: false,
    environmental_weight: 0.4,
    social_weight: 0.3,
    governance_weight: 0.3,
  });

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (config) {
      setFormData({
        auto_emission_calculation: config.auto_emission_calculation,
        require_evidence_for_csr: config.require_evidence_for_csr,
        environmental_weight: config.environmental_weight,
        social_weight: config.social_weight,
        governance_weight: config.governance_weight,
      });
    }
  }, [config]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : parseFloat(value) || 0
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const total = formData.environmental_weight + formData.social_weight + formData.governance_weight;
    if (Math.abs(total - 1.0) > 0.001) {
      setError(`Weights must sum to exactly 1.0. Current sum is ${total.toFixed(2)}.`);
      return;
    }

    updateConfig.mutate(formData, {
      onError: (err: any) => {
        setError(err.message || 'Failed to update configuration.');
      },
      onSuccess: () => {
        alert('Configuration saved successfully!');
      }
    });
  };

  if (isLoading) {
    return <div className="text-slate-400 py-8 text-center">Loading configuration...</div>;
  }

  const currentSum = formData.environmental_weight + formData.social_weight + formData.governance_weight;
  const isSumValid = Math.abs(currentSum - 1.0) <= 0.001;

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold text-slate-100">Global ESG Configuration</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        
        {/* Feature Toggles */}
        <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-700/50 space-y-6">
          <h3 className="text-lg font-medium text-slate-200">Feature Toggles</h3>
          
          <label className="flex items-start space-x-4 cursor-pointer group">
            <div className="relative flex items-center justify-center mt-1">
              <input
                type="checkbox"
                name="auto_emission_calculation"
                checked={formData.auto_emission_calculation}
                onChange={handleChange}
                className="peer sr-only"
              />
              <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-emerald-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
            </div>
            <div>
              <div className="text-slate-200 font-medium group-hover:text-white transition-colors">Auto Emission Calculation</div>
              <div className="text-slate-400 text-sm mt-1">Automatically create carbon transactions when operational records are added.</div>
            </div>
          </label>

          <label className="flex items-start space-x-4 cursor-pointer group">
            <div className="relative flex items-center justify-center mt-1">
              <input
                type="checkbox"
                name="require_evidence_for_csr"
                checked={formData.require_evidence_for_csr}
                onChange={handleChange}
                className="peer sr-only"
              />
              <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-emerald-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500"></div>
            </div>
            <div>
              <div className="text-slate-200 font-medium group-hover:text-white transition-colors">Require Evidence for CSR</div>
              <div className="text-slate-400 text-sm mt-1">Employees must provide a proof URL before a CSR participation can be approved.</div>
            </div>
          </label>
        </div>

        {/* ESG Weights */}
        <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-700/50 space-y-6">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-medium text-slate-200">Scoring Weights</h3>
              <p className="text-slate-400 text-sm mt-1">Adjust the weights for calculating the overall ESG score. Must sum to exactly 1.00.</p>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium border ${
              isSumValid ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-red-500/10 text-red-400 border-red-500/20'
            }`}>
              Sum: {currentSum.toFixed(2)}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300 block">Environmental (E)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name="environmental_weight"
                value={formData.environmental_weight}
                onChange={handleChange}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300 block">Social (S)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name="social_weight"
                value={formData.social_weight}
                onChange={handleChange}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300 block">Governance (G)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name="governance_weight"
                value={formData.governance_weight}
                onChange={handleChange}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>
        </div>

        {error && (
          <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-sm">
            {error}
          </div>
        )}

        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={updateConfig.isPending || !isSumValid}
            className="px-6 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-lg shadow-[0_0_15px_rgba(16,185,129,0.3)] hover:shadow-[0_0_25px_rgba(16,185,129,0.5)] transition-all disabled:opacity-50 disabled:shadow-none"
          >
            {updateConfig.isPending ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </form>
    </div>
  );
}
