import { Link } from 'react-router-dom';
import { Shield, MapPin, Zap, Mic, Bell, Waypoints } from 'lucide-react';
import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import Button from '../components/ui/button.jsx';
import FeatureCard from '../components/ui/feature-card.jsx';
import MapContainer from '../components/map/map-container.jsx';
import { dummyAlerts, dummySafeSpots, dummySafeZones, dummyUnsafeZones } from '../utils/dummy-data.js';

function Landing() {
  const totalAlerts = dummyAlerts.length;
  const highSeverityAlerts = dummyAlerts.filter((alert) => alert.severity === 'high').length;
  const totalSafeSpots = dummySafeSpots.length;

  const features = [
    {
      icon: <Bell className="h-4 w-4" />,
      title: 'Real-time safety alerts',
      description: 'Surface hyper-local alerts about harassment, suspicious activity and patrols in seconds.',
      badge: 'Alert intelligence',
    },
    {
      icon: <Waypoints className="h-4 w-4" />,
      title: 'Smart night routes',
      description: 'Safer night-time routing using safer streets, active patrols and community presence.',
      badge: 'Night safety',
    },
    {
      icon: <Mic className="h-4 w-4" />,
      title: 'Voice & motion SOS',
      description: 'Trigger SOS hands-free via voice or shake gestures. Frontend-only for now, AI-ready.',
      badge: 'SOS automation',
    },
  ];

  return (
    <div className="space-y-12">
      <section className="grid gap-10 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] lg:items-center">
        <AnimatedWrapper direction="up" delay={0.02} className="space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full bg-primary-600/10 px-3 py-1 text-[11px] font-medium uppercase tracking-wide text-primary-700 dark:text-primary-300">
            <Shield className="h-3 w-3" />
            <span>AI-ready safety intelligence, frontend-only demo</span>
          </div>
          <h1 className="text-balance text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl lg:text-5xl dark:text-slate-50">
            Safe-Zone for women & students,
            <span className="text-primary-600 dark:text-primary-400"> powered by safety data.</span>
          </h1>
          <p className="max-w-2xl text-sm leading-relaxed text-slate-600 dark:text-slate-300">
            Safe-Zone turns raw alerts, safe spots and campus signals into real-time guidance. This
            UI is wired to dummy data only but designed to connect directly to your backend and AI
            models with zero redesign.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <Link to="/signup">
              <Button size="lg" className="px-6 text-sm">
                Get started in demo mode
              </Button>
            </Link>
            <Link to="/dashboard">
              <Button variant="ghost" size="lg" className="text-sm">
                View safety dashboard
              </Button>
            </Link>
          </div>
          <div className="mt-4 grid gap-4 text-xs text-slate-600 sm:grid-cols-3 dark:text-slate-300">
            <div className="flex items-center gap-2 rounded-xl bg-white/80 px-3 py-2 shadow-sm ring-1 ring-slate-200/70 dark:bg-slate-900/80 dark:ring-slate-800/80">
              <Bell className="h-4 w-4 text-primary-600" />
              <div>
                <p className="font-semibold">{totalAlerts}</p>
                <p className="text-[11px]">Live alerts (dummy)</p>
              </div>
            </div>
            <div className="flex items-center gap-2 rounded-xl bg-white/80 px-3 py-2 shadow-sm ring-1 ring-slate-200/70 dark:bg-slate-900/80 dark:ring-slate-800/80">
              <Zap className="h-4 w-4 text-amber-500" />
              <div>
                <p className="font-semibold">{highSeverityAlerts}</p>
                <p className="text-[11px]">High severity hotspots</p>
              </div>
            </div>
            <div className="flex items-center gap-2 rounded-xl bg-white/80 px-3 py-2 shadow-sm ring-1 ring-slate-200/70 dark:bg-slate-900/80 dark:ring-slate-800/80">
              <MapPin className="h-4 w-4 text-emerald-500" />
              <div>
                <p className="font-semibold">{totalSafeSpots}</p>
                <p className="text-[11px]">Verified safe spots</p>
              </div>
            </div>
          </div>
        </AnimatedWrapper>

        <AnimatedWrapper direction="left" delay={0.06} className="space-y-4">
          <MapContainer
            safeZones={dummySafeZones}
            unsafeZones={dummyUnsafeZones}
            safeSpots={dummySafeSpots}
          />
        </AnimatedWrapper>
      </section>

      <section className="space-y-4">
        <AnimatedWrapper>
          <h2 className="text-lg font-semibold tracking-tight text-slate-900 dark:text-slate-50">
            Why Safe-Zone?
          </h2>
          <p className="max-w-2xl text-sm text-slate-600 dark:text-slate-300">
            Built for campuses and cities that care about women and student safety. Safe-Zone is a
            modular safety layer that your backend and AI team can integrate without touching the
            UI.
          </p>
        </AnimatedWrapper>
        <div className="grid gap-4 md:grid-cols-3">
          {features.map((feature, index) => (
            <AnimatedWrapper key={feature.title} delay={0.05 * index}>
              <FeatureCard
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                badge={feature.badge}
              />
            </AnimatedWrapper>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Landing;
