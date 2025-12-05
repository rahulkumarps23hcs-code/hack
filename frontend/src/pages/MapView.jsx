import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card.jsx';
import MapContainer from '../components/map/map-container.jsx';
import SafeSpotCard from '../components/safe-spots/safe-spot-card.jsx';
import { dummySafeSpots, dummySafeZones, dummyUnsafeZones } from '../utils/dummy-data.js';

function MapView() {
  return (
    <div className="space-y-6">
      <AnimatedWrapper>
        <div className="space-y-1">
          <h1 className="text-xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">
            Safety map
          </h1>
          <p className="text-xs text-slate-600 dark:text-slate-300">
            Visualise safe corridors, sensitive zones and trusted safe spots. All coordinates are
            dummy, the layout is ready for a real map SDK.
          </p>
        </div>
      </AnimatedWrapper>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]">
        <AnimatedWrapper direction="up" delay={0.02}>
          <MapContainer
            safeZones={dummySafeZones}
            unsafeZones={dummyUnsafeZones}
            safeSpots={dummySafeSpots}
          />
        </AnimatedWrapper>

        <AnimatedWrapper direction="left" delay={0.06}>
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Nearest safe spots</CardTitle>
              <CardDescription>
                These are mock safe spots that a real GET /safe-spots would return.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 max-h-[360px] overflow-y-auto pr-1">
              {dummySafeSpots.map((spot) => (
                <SafeSpotCard key={spot.id} spot={spot} />
              ))}
            </CardContent>
          </Card>
        </AnimatedWrapper>
      </div>
    </div>
  );
}

export default MapView;
