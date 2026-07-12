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
    return <div className="text-muted-foreground py-8 text-center text-small">Loading configuration...</div>;
  }

  const currentSum = formData.environmental_weight + formData.social_weight + formData.governance_weight;
  const isSumValid = Math.abs(currentSum - 1.0) <= 0.001;

  return (
    <div className="space-y-8 max-w-3xl">
      <h2 className="text-h4 font-medium text-foreground">Global ESG Configuration</h2>

      <form onSubmit={handleSubmit} className="space-y-8">
        
        {/* Feature Toggles */}
        <div className="space-y-6">
          <h3 className="text-body font-semibold text-foreground border-b border-border pb-2">Feature Toggles</h3>
          
          <label className="flex items-start gap-4 cursor-pointer group">
            <div className="relative flex items-center justify-center mt-0.5">
              <input
                type="checkbox"
                name="auto_emission_calculation"
                checked={formData.auto_emission_calculation}
                onChange={handleChange}
                className="peer sr-only"
              />
              <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary border border-border peer-checked:border-primary"></div>
            </div>
            <div>
              <div className="text-small font-medium text-foreground transition-colors">Auto Emission Calculation</div>
              <div className="text-caption text-muted-foreground mt-1">Automatically create carbon transactions when operational records are added.</div>
            </div>
          </label>

          <label className="flex items-start gap-4 cursor-pointer group">
            <div className="relative flex items-center justify-center mt-0.5">
              <input
                type="checkbox"
                name="require_evidence_for_csr"
                checked={formData.require_evidence_for_csr}
                onChange={handleChange}
                className="peer sr-only"
              />
              <div className="w-11 h-6 bg-muted peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary border border-border peer-checked:border-primary"></div>
            </div>
            <div>
              <div className="text-small font-medium text-foreground transition-colors">Require Evidence for CSR</div>
              <div className="text-caption text-muted-foreground mt-1">Employees must provide a proof URL before a CSR participation can be approved.</div>
            </div>
          </label>
        </div>

        {/* ESG Weights */}
        <div className="space-y-6">
          <div className="flex justify-between items-start border-b border-border pb-2">
            <div>
              <h3 className="text-body font-semibold text-foreground">Scoring Weights</h3>
              <p className="text-caption text-muted-foreground mt-1">Adjust the weights for calculating the overall ESG score. Must sum to exactly 1.00.</p>
            </div>
            <div className={`px-2.5 py-1 rounded-full text-caption font-medium border ${
              isSumValid ? 'bg-success/10 text-success border-success/20' : 'bg-destructive/10 text-destructive border-destructive/20'
            }`}>
              Sum: {currentSum.toFixed(2)}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label className="text-small font-medium text-foreground block">Environmental (E)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name="environmental_weight"
                value={formData.environmental_weight}
                onChange={handleChange}
                className="w-full bg-muted border-none rounded-[var(--radius-input)] px-4 py-2 text-small text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>
            <div className="space-y-2">
              <label className="text-small font-medium text-foreground block">Social (S)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name="social_weight"
                value={formData.social_weight}
                onChange={handleChange}
                className="w-full bg-muted border-none rounded-[var(--radius-input)] px-4 py-2 text-small text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>
            <div className="space-y-2">
              <label className="text-small font-medium text-foreground block">Governance (G)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name="governance_weight"
                value={formData.governance_weight}
                onChange={handleChange}
                className="w-full bg-muted border-none rounded-[var(--radius-input)] px-4 py-2 text-small text-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>
          </div>
        </div>

        {error && (
          <div className="p-3 bg-destructive/10 border border-destructive/20 text-destructive rounded-[var(--radius-input)] text-small">
            {error}
          </div>
        )}

        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={updateConfig.isPending || !isSumValid}
            className="px-6 py-2 bg-primary hover:bg-primary/90 text-white font-medium text-small rounded-[var(--radius-btn)] transition-all disabled:opacity-50"
          >
            {updateConfig.isPending ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </form>
    </div>
  );
}
