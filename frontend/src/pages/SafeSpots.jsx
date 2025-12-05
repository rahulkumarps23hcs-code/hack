import { useMemo, useState } from 'react';
import { MapPin, Filter, ShieldCheck } from 'lucide-react';
import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card.jsx';
import SafeSpotCard from '../components/safe-spots/safe-spot-card.jsx';
import MapContainer from '../components/map/map-container.jsx';
import { dummySafeSpots, dummySafeZones, dummyUnsafeZones } from '../utils/dummy-data.js';

function SafeSpots() {
  const [typeFilter, setTypeFilter] = useState('all');

  const uniqueTypes = useMemo(() => {
    const types = new Set(dummySafeSpots.map((spot) => spot.type));
    return Array.from(types);
  }, []);

  const filteredSpots = useMemo(() => {
    if (typeFilter === 'all') {
      return dummySafeSpots;
    }
    return dummySafeSpots.filter((spot) => spot.type === typeFilter);
  }, [typeFilter]);

  return (
    <div className="space-y-6">
      <AnimatedWrapper>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">
              Nearest safe spots
            </h1>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Pharmacies, security kiosks, help centres and more. This uses dummy data but mirrors a
              production GET /safe-spots integration.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-[11px] text-slate-600 dark:bg-slate-900 dark:text-slate-300">
            <ShieldCheck className="h-3 w-3 text-emerald-500" />
            <span>{dummySafeSpots.length} verified safe spots (demo)</span>
          </div>
        </div>
      </AnimatedWrapper>

      <AnimatedWrapper delay={0.02}>
        <Card>
          <CardHeader className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <CardTitle>Filters</CardTitle>
              <CardDescription>Filter safe spots by category.</CardDescription>
            </div>
            <div className="flex flex-wrap items-center gap-2 text-[11px] text-slate-600 dark:text-slate-300">
              <Filter className="h-3 w-3" />
              <button
                type="button"
                onClick={() => setTypeFilter('all')}
                className={`rounded-full px-2 py-0.5 ${
                  typeFilter === 'all'
                    ? 'bg-primary-600 text-white'
                    : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                }`}
              >
                All
              </button>
              {uniqueTypes.map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setTypeFilter(type)}
                  className={`rounded-full px-2 py-0.5 capitalize ${
                    typeFilter === type
                      ? 'bg-emerald-500 text-white'
                      : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                  }`}
                >
                  {type.replace('-', ' ')}
                </button>
              ))}
            </div>
          </CardHeader>
        </Card>
      </AnimatedWrapper>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
        <AnimatedWrapper direction="up" delay={0.04}>
          <Card>
            <CardHeader>
              <CardTitle>Safe spot list</CardTitle>
              <CardDescription>Scroll through nearby safe locations.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 max-h-[420px] overflow-y-auto pr-1">
              {filteredSpots.map((spot) => (
                <SafeSpotCard key={spot.id} spot={spot} />
              ))}
            </CardContent>
          </Card>
        </AnimatedWrapper>

        <AnimatedWrapper direction="left" delay={0.06}>
          <Card>
            <CardHeader>
              <CardTitle>Safe spots on map</CardTitle>
              <CardDescription>
                Dummy map projection of safe and unsafe zones your backend would provide.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-2 flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400">
                <MapPin className="h-3 w-3" />
                <span>Integrate any WebGL/JS map SDK in place of this static container.</span>
              </div>
              <MapContainer
                safeZones={dummySafeZones}
                unsafeZones={dummyUnsafeZones}
                safeSpots={dummySafeSpots}
              />
            </CardContent>
          </Card>
        </AnimatedWrapper>
      </div>
    </div>
  );
}

export default SafeSpots;
