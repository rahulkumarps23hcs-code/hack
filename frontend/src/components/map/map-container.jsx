import { MapPin, Shield, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card.jsx';

function MapContainer({ safeZones = [], unsafeZones = [], safeSpots = [] }) {
  return (
    <Card className="h-full min-h-[260px] bg-gradient-to-b from-slate-900 via-slate-950 to-slate-900 text-slate-50">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle className="text-slate-50">Safety heatmap</CardTitle>
            <CardDescription className="text-slate-400">
              Visual representation of safe and sensitive areas (dummy layout).
            </CardDescription>
          </div>
          <div className="flex items-center gap-2 text-[11px] text-slate-300">
            <span className="inline-flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-emerald-400" /> Safe
            </span>
            <span className="inline-flex items-center gap-1">
              <span className="h-2 w-2 rounded-full bg-red-400" /> Sensitive
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative h-64 w-full overflow-hidden rounded-lg bg-[radial-gradient(circle_at_top,_#1d283a,_#020617)]">
          <div className="absolute inset-6 rounded-lg border border-slate-700/60" />
          {safeZones.map((zone) => (
            <div
              key={zone.id}
              className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1 text-[10px] text-emerald-100"
              style={{ left: `${48 + (zone.location.lng % 4) * 10}%`, top: `${30 + (zone.location.lat % 4) * 8}%` }}
            >
              <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500/80 shadow-soft">
                <Shield className="h-3 w-3" />
              </span>
              <span className="max-w-[80px] truncate text-center">{zone.name}</span>
            </div>
          ))}
          {unsafeZones.map((zone) => (
            <div
              key={zone.id}
              className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1 text-[10px] text-red-100"
              style={{ left: `${40 + (zone.location.lng % 5) * 9}%`, top: `${40 + (zone.location.lat % 5) * 7}%` }}
            >
              <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-red-500/80 shadow-soft">
                <AlertTriangle className="h-3 w-3" />
              </span>
              <span className="max-w-[80px] truncate text-center">{zone.name}</span>
            </div>
          ))}
          {safeSpots.slice(0, 4).map((spot, index) => (
            <div
              key={spot.id}
              className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1 text-[10px] text-sky-100"
              style={{ left: `${30 + index * 15}%`, top: `${25 + index * 10}%` }}
            >
              <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-sky-500/80 shadow-soft">
                <MapPin className="h-3 w-3" />
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export default MapContainer;
