import { useMemo, useState } from 'react';
import { Filter, PlusCircle, AlertTriangle } from 'lucide-react';
import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card.jsx';
import Button from '../components/ui/button.jsx';
import InputField from '../components/ui/input-field.jsx';
import AlertCard from '../components/alerts/alert-card.jsx';
import Modal from '../components/ui/modal.jsx';
import { useAlerts } from '../context/alert-context.jsx';
import { useToast } from '../context/toast-context.jsx';

function Alerts() {
  const { alerts, filteredAlerts, severityFilter, setSeverityFilter } = useAlerts();
  const { addToast } = useToast();

  const [isReporting, setIsReporting] = useState(false);
  const [reportForm, setReportForm] = useState({ type: '', description: '' });
  const [reportErrors, setReportErrors] = useState({});

  const countsBySeverity = useMemo(() => {
    return alerts.reduce(
      (acc, alert) => {
        acc[alert.severity] += 1;
        return acc;
      },
      { low: 0, medium: 0, high: 0 }
    );
  }, [alerts]);

  const handleFilterChange = (value) => {
    setSeverityFilter(value);
  };

  const handleReportChange = (event) => {
    const { name, value } = event.target;
    setReportForm((prev) => ({ ...prev, [name]: value }));
  };

  const validateReport = () => {
    const nextErrors = {};
    if (!reportForm.type) {
      nextErrors.type = 'Type is required';
    }
    if (!reportForm.description) {
      nextErrors.description = 'Description is required';
    }
    setReportErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleReportSubmit = (event) => {
    event.preventDefault();
    if (!validateReport()) {
      return;
    }
    addToast({
      variant: 'success',
      title: 'Report submitted (demo)',
      description: 'In production, this would create a new alert via POST /alerts/report.',
    });
    setIsReporting(false);
    setReportForm({ type: '', description: '' });
  };

  return (
    <div className="space-y-6">
      <AnimatedWrapper>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">
              Real-time alerts
            </h1>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Streaming safety intelligence with filters and community reporting. All data here is
              dummy, but the integration surface is production-grade.
            </p>
          </div>
          <Button size="sm" variant="outline" onClick={() => setIsReporting(true)}>
            <PlusCircle className="mr-1.5 h-3 w-3" />
            Report an incident
          </Button>
        </div>
      </AnimatedWrapper>

      <AnimatedWrapper delay={0.02}>
        <Card>
          <CardHeader className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <CardTitle>Filters</CardTitle>
              <CardDescription>Focus on the alerts most relevant to your risk level.</CardDescription>
            </div>
            <div className="flex flex-wrap items-center gap-2 text-[11px] text-slate-600 dark:text-slate-300">
              <Filter className="h-3 w-3" />
              <button
                type="button"
                onClick={() => handleFilterChange('all')}
                className={`rounded-full px-2 py-0.5 ${
                  severityFilter === 'all'
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                }`}
              >
                All
              </button>
              <button
                type="button"
                onClick={() => handleFilterChange('high')}
                className={`rounded-full px-2 py-0.5 ${
                  severityFilter === 'high'
                    ? 'bg-danger-500 text-white'
                    : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                }`}
              >
                High ({countsBySeverity.high})
              </button>
              <button
                type="button"
                onClick={() => handleFilterChange('medium')}
                className={`rounded-full px-2 py-0.5 ${
                  severityFilter === 'medium'
                    ? 'bg-amber-500 text-white'
                    : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                }`}
              >
                Medium ({countsBySeverity.medium})
              </button>
              <button
                type="button"
                onClick={() => handleFilterChange('low')}
                className={`rounded-full px-2 py-0.5 ${
                  severityFilter === 'low'
                    ? 'bg-emerald-500 text-white'
                    : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                }`}
              >
                Low ({countsBySeverity.low})
              </button>
            </div>
          </CardHeader>
        </Card>
      </AnimatedWrapper>

      <AnimatedWrapper delay={0.04}>
        <div className="grid gap-4 md:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]">
          <Card>
            <CardHeader className="flex items-center justify-between">
              <div>
                <CardTitle>Alert feed</CardTitle>
                <CardDescription>
                  Ordered by recency. In production this would stream from GET /alerts.
                </CardDescription>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {filteredAlerts.map((alert) => (
                <AlertCard key={alert.id} alert={alert} />
              ))}
              {filteredAlerts.length === 0 && (
                <p className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                  <AlertTriangle className="h-3 w-3" />
                  <span>No alerts match the current filters.</span>
                </p>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>How community reporting works</CardTitle>
              <CardDescription>
                This panel explains the incident pipeline for women & student safety.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 text-xs text-slate-600 dark:text-slate-200">
              <p>
                1. A student or guardian reports an incident with basic details and optional
                location.
              </p>
              <p>
                2. The backend validates, anonymises and enriches this report with threat
                intelligence.
              </p>
              <p>3. Safe-Zone surfaces the alert to at-risk users as a contextual notification.</p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                In this demo, submitting the form simply shows a toast and does not send any data.
              </p>
            </CardContent>
          </Card>
        </div>
      </AnimatedWrapper>

      <Modal
        isOpen={isReporting}
        onClose={() => setIsReporting(false)}
        title="Report an incident (demo)"
        description="Simulate a POST /alerts/report request. No data leaves your browser."
        size="md"
        actions={
          <>
            <Button variant="ghost" size="sm" onClick={() => setIsReporting(false)}>
              Cancel
            </Button>
            <Button size="sm" onClick={handleReportSubmit}>
              Submit report
            </Button>
          </>
        }
      >
        <form className="space-y-3" onSubmit={handleReportSubmit}>
          <InputField
            id="type"
            name="type"
            label="Incident type"
            placeholder="e.g. harassment, stalking, suspicious activity"
            value={reportForm.type}
            onChange={handleReportChange}
            error={reportErrors.type}
          />
          <InputField
            id="description"
            name="description"
            label="What happened?"
            placeholder="Add a brief, anonymised description of what you experienced or observed."
            value={reportForm.description}
            onChange={handleReportChange}
            error={reportErrors.description}
          />
        </form>
      </Modal>
    </div>
  );
}

export default Alerts;
