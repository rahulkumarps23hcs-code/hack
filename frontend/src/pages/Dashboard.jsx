import { useMemo } from 'react';
import { Activity, Bell, MapPin, ShieldCheck, Clock } from 'lucide-react';
import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '../components/ui/card.jsx';
import LoadingSkeleton from '../components/ui/loading-skeleton.jsx';
import AlertCard from '../components/alerts/alert-card.jsx';
import SafeSpotCard from '../components/safe-spots/safe-spot-card.jsx';
import { useAuth } from '../context/auth-context.jsx';
import { useAlerts } from '../context/alert-context.jsx';
import { useNightSafety } from '../hooks/use-night-safety.js';
import { dummyUserHistory, dummySafeSpots } from '../utils/dummy-data.js';

function Dashboard() {
  const { user, initializing } = useAuth();
  const { alerts, filteredAlerts } = useAlerts();
  const nightSafety = useNightSafety();

  const safetyRingGradient =
    nightSafety.safetyScore < 50
      ? 'from-danger-500 via-amber-500 to-red-500'
      : nightSafety.safetyScore < 75
      ? 'from-amber-400 via-primary-500 to-amber-500'
      : 'from-emerald-400 via-primary-500 to-emerald-400';

  const latestAlerts = useMemo(() => filteredAlerts.slice(0, 3), [filteredAlerts]);
  const highSeverityCount = useMemo(
    () => alerts.filter((alert) => alert.severity === 'high').length,
    [alerts]
  );
  const mediumSeverityCount = useMemo(
    () => alerts.filter((alert) => alert.severity === 'medium').length,
    [alerts]
  );
  const topSafeSpots = useMemo(() => dummySafeSpots.slice(0, 3), []);

  if (initializing) {
    return (
      <div className="grid gap-4 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
        <LoadingSkeleton className="h-40 rounded-2xl" />
        <LoadingSkeleton className="h-40 rounded-2xl" />
      </div>
    );
  }

  return (
    <div className="space-y-6 lg:space-y-8">
      {/* Hero banner */}
      <AnimatedWrapper>
        <div className="relative flex flex-wrap items-center justify-between gap-4 overflow-hidden rounded-2xl bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-4 py-4 text-slate-50 shadow-[0_22px_65px_rgba(15,23,42,0.95)] ring-1 ring-slate-800/80 backdrop-blur-2xl sm:px-6 sm:py-5">
          <div className="pointer-events-none absolute -left-10 -top-12 h-32 w-32 rounded-full bg-primary-500/25 blur-3xl" />
          <div className="pointer-events-none absolute -right-16 bottom-[-40px] h-40 w-40 rounded-full bg-emerald-500/25 blur-3xl" />

          <div className="relative space-y-2">
            <h1 className="text-xl font-semibold tracking-tight sm:text-2xl">
              Hi {user?.name ?? 'there'}, your safety overview
            </h1>
            <p className="max-w-xl text-xs text-slate-300 sm:text-sm">
              Safety intelligence for women & students, running in a frontend-only demo mode.
            </p>
            <div className="inline-flex items-center gap-1 rounded-full bg-slate-900/70 px-2.5 py-1 text-[10px] text-slate-300">
              <Activity className="h-3 w-3 text-emerald-400" />
              <span>Demo data · ready for AI + backend integration</span>
            </div>
          </div>

          <div className="relative flex items-center gap-2 rounded-full bg-slate-900/80 px-3 py-1.5 text-[11px] text-slate-200 backdrop-blur-sm">
            <Clock className="h-3 w-3 text-emerald-400" />
            <span>Smart Night Mode: {nightSafety.isNight ? 'Active' : 'Daytime mode'}</span>
          </div>
        </div>
      </AnimatedWrapper>

      {/* Stat strip */}
      <AnimatedWrapper delay={0.04}>
        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <div className="group relative overflow-hidden rounded-2xl border border-slate-200/70 bg-white/75 px-4 py-3 text-xs shadow-[0_18px_45px_rgba(15,23,42,0.2)] backdrop-blur-xl transition hover:-translate-y-1 hover:border-primary-500/80 hover:shadow-[0_24px_80px_rgba(79,70,229,0.45)] dark:border-slate-800/80 dark:bg-slate-950/80">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-500/0 via-primary-500/15 to-primary-500/0 opacity-0 transition group-hover:opacity-100" />
            <div className="relative flex items-center justify-between gap-3">
              <div className="space-y-1">
                <p className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
                  Active alerts
                </p>
                <p className="text-lg font-semibold text-slate-900 dark:text-slate-50">
                  {alerts.length}
                </p>
              </div>
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-primary-600/10 text-primary-600">
                <Bell className="h-4 w-4" />
              </span>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-slate-200/70 bg-white/75 px-4 py-3 text-xs shadow-[0_18px_45px_rgba(15,23,42,0.2)] backdrop-blur-xl transition hover:-translate-y-1 hover:border-danger-500/80 hover:shadow-[0_24px_80px_rgba(239,68,68,0.45)] dark:border-slate-800/80 dark:bg-slate-950/80">
            <div className="absolute inset-0 bg-gradient-to-r from-danger-500/0 via-danger-500/15 to-danger-500/0 opacity-0 transition group-hover:opacity-100" />
            <div className="relative flex items-center justify-between gap-3">
              <div className="space-y-1">
                <p className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
                  High-risk alerts
                </p>
                <p className="text-lg font-semibold text-slate-900 dark:text-slate-50">
                  {highSeverityCount}
                </p>
              </div>
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-danger-500/10 text-danger-500">
                <Activity className="h-4 w-4" />
              </span>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-slate-200/70 bg-white/75 px-4 py-3 text-xs shadow-[0_18px_45px_rgba(15,23,42,0.2)] backdrop-blur-xl transition hover:-translate-y-1 hover:border-emerald-500/80 hover:shadow-[0_24px_80px_rgba(16,185,129,0.45)] dark:border-slate-800/80 dark:bg-slate-950/80">
            <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/0 via-emerald-500/15 to-emerald-500/0 opacity-0 transition group-hover:opacity-100" />
            <div className="relative flex items-center justify-between gap-3">
              <div className="space-y-1">
                <p className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
                  Verified safe spots
                </p>
                <p className="text-lg font-semibold text-slate-900 dark:text-slate-50">
                  {dummySafeSpots.length}
                </p>
              </div>
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-500">
                <MapPin className="h-4 w-4" />
              </span>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-2xl border border-slate-200/70 bg-white/75 px-4 py-3 text-xs shadow-[0_18px_45px_rgba(15,23,42,0.2)] backdrop-blur-xl transition hover:-translate-y-1 hover:border-amber-500/80 hover:shadow-[0_24px_80px_rgba(245,158,11,0.45)] dark:border-slate-800/80 dark:bg-slate-950/80">
            <div className="absolute inset-0 bg-gradient-to-r from-amber-500/0 via-amber-500/15 to-amber-500/0 opacity-0 transition group-hover:opacity-100" />
            <div className="relative flex items-center justify-between gap-3">
              <div className="space-y-1">
                <p className="text-[11px] font-medium text-slate-500 dark:text-slate-400">
                  Medium-risk alerts
                </p>
                <p className="text-lg font-semibold text-slate-900 dark:text-slate-50">
                  {mediumSeverityCount}
                </p>
              </div>
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-amber-500/10 text-amber-500">
                <ShieldCheck className="h-4 w-4" />
              </span>
            </div>
          </div>
        </div>
      </AnimatedWrapper>

      {/* Night safety + key signals */}
      <div className="grid gap-4 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] lg:items-start">
        <AnimatedWrapper direction="up" delay={0.06}>
          <Card className="relative overflow-hidden border-none bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-50 shadow-[0_26px_80px_rgba(15,23,42,0.95)] ring-1 ring-slate-800/80 backdrop-blur-2xl">
            <div className="pointer-events-none absolute -right-24 top-10 h-40 w-40 rounded-full bg-primary-500/25 blur-3xl" />
            <CardHeader className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="space-y-1">
                <CardTitle>Night safety signal</CardTitle>
                <CardDescription>
                  Personalised safety context for your current area (mock geolocation only).
                </CardDescription>
                <p className="text-[11px] text-slate-300">
                  {nightSafety.location.city}, {nightSafety.location.area}
                </p>
              </div>
              <div className="flex items-center gap-4">
                <div className="relative flex h-20 w-20 items-center justify-center">
                  <div
                    className={`absolute inset-0 rounded-full bg-gradient-to-tr ${safetyRingGradient} opacity-80`}
                  />
                  <div className="absolute inset-[4px] rounded-full bg-slate-950" />
                  <div className="relative text-center">
                    <p className="text-lg font-semibold leading-tight">{nightSafety.safetyScore}</p>
                    <p className="text-[10px] text-slate-400">safety</p>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-xs text-slate-100/90 sm:text-sm">
                {nightSafety.primaryMessage}
              </p>
              <p className="text-[11px] text-slate-300">
                {nightSafety.secondaryMessage}
              </p>
              <div className="relative mt-1 h-1.5 w-full overflow-hidden rounded-full bg-slate-800/80">
                <div
                  className="h-full rounded-full bg-emerald-400"
                  style={{ width: `${nightSafety.safetyScore}%` }}
                />
              </div>
              <div className="mt-3 flex flex-wrap gap-2 text-[11px] text-slate-200/90">
                <span className="inline-flex items-center gap-1 rounded-full bg-slate-900/70 px-2.5 py-1">
                  <Activity className="h-3 w-3" />
                  <span>
                    {nightSafety.isNight
                      ? 'Night-time conditions are in effect.'
                      : 'Daytime profile.'}
                  </span>
                </span>
              </div>
            </CardContent>
          </Card>
        </AnimatedWrapper>

        <AnimatedWrapper direction="left" delay={0.08}>
          <Card className="border border-slate-800/80 bg-slate-950/90 text-slate-50 shadow-[0_22px_70px_rgba(15,23,42,0.85)] backdrop-blur-xl">
            <CardHeader className="flex items-center justify-between gap-3">
              <div>
                <CardTitle>Key signals</CardTitle>
                <CardDescription className="text-[11px] text-slate-400">
                  Snapshot of your recent activity in Safe-Zone.
                </CardDescription>
              </div>
            </CardHeader>
            <CardContent className="grid gap-3 text-xs text-slate-200">
              <div className="flex items-center justify-between gap-3 rounded-2xl border border-slate-800/80 bg-slate-900/80 px-3 py-2.5 transition hover:-translate-y-0.5 hover:border-slate-500/80">
                <div className="flex items-center gap-2">
                  <Bell className="h-4 w-4 text-primary-400" />
                  <span>Alerts visible in your feed</span>
                </div>
                <span className="text-sm font-semibold">{alerts.length}</span>
              </div>
              <div className="flex items-center justify-between gap-3 rounded-2xl border border-slate-800/80 bg-slate-900/80 px-3 py-2.5 transition hover:-translate-y-0.5 hover:border-slate-500/80">
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-emerald-500" />
                  <span>Safe spots in 2km radius (dummy)</span>
                </div>
                <span className="text-sm font-semibold">{dummySafeSpots.length}</span>
              </div>
              <div className="flex items-center justify-between gap-3 rounded-2xl border border-slate-800/80 bg-slate-900/80 px-3 py-2.5 transition hover:-translate-y-0.5 hover:border-slate-500/80">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="h-4 w-4 text-emerald-500" />
                  <span>Last SOS or check-in event</span>
                </div>
                <span className="max-w-[140px] truncate text-right">
                  {dummyUserHistory[0]?.description ?? 'No history yet'}
                </span>
              </div>
              <div className="mt-2 space-y-1 border-t border-slate-800/80 pt-2 text-[11px] text-slate-400">
                {dummyUserHistory.slice(0, 3).map((item) => (
                  <div key={item.id} className="flex items-start gap-2">
                    <Clock className="mt-[2px] h-3 w-3 text-slate-500" />
                    <div className="space-y-0.5">
                      <p className="text-[11px] text-slate-200">{item.description}</p>
                      <p className="text-[10px] text-slate-500">
                        {new Date(item.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </AnimatedWrapper>
      </div>

      {/* Alert feed + safe spots */}
      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
        <AnimatedWrapper direction="up" delay={0.1}>
          <Card className="h-full rounded-2xl border border-slate-200/70 bg-white/90 shadow-[0_20px_60px_rgba(15,23,42,0.12)] backdrop-blur-xl dark:border-slate-800/80 dark:bg-slate-950/90">
            <CardHeader className="flex items-center justify-between">
              <div>
                <CardTitle>Latest alerts</CardTitle>
                <CardDescription>High-signal alerts affecting your nearby area.</CardDescription>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {latestAlerts.map((alert) => (
                <AlertCard key={alert.id} alert={alert} />
              ))}
              {latestAlerts.length === 0 && (
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  No alerts found. This is expected in a demo environment.
                </p>
              )}
            </CardContent>
          </Card>
        </AnimatedWrapper>

        <AnimatedWrapper direction="left" delay={0.12}>
          <Card className="h-full rounded-2xl border border-slate-200/70 bg-white/90 shadow-[0_20px_60px_rgba(15,23,42,0.12)] backdrop-blur-xl dark:border-slate-800/80 dark:bg-slate-950/90">
            <CardHeader>
              <CardTitle>Nearby safe spots</CardTitle>
              <CardDescription>
                Nearest pharmacies, kiosks and safe waiting areas (dummy locations only).
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {topSafeSpots.map((spot) => (
                <SafeSpotCard key={spot.id} spot={spot} />
              ))}
            </CardContent>
          </Card>
        </AnimatedWrapper>
      </div>
    </div>
  );
}

export default Dashboard;
