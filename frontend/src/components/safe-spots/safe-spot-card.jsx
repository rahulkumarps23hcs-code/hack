import { MapPin, ShieldCheck, Navigation } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card.jsx';
import Badge from '../ui/badge.jsx';

function SafeSpotCard({ spot }) {
  if (!spot) {
    return null;
  }

  const { name, type, address, location } = spot;

  return (
    <Card className="flex flex-col gap-3">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div className="space-y-1">
            <CardTitle className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-success-500" />
              <span>{name}</span>
            </CardTitle>
            <CardDescription className="capitalize">{type.replace('-', ' ')}</CardDescription>
          </div>
          <Badge variant="outline" className="capitalize">
            Safe spot
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 text-xs text-slate-600 dark:text-slate-200">
          <div className="flex items-start gap-2">
            <MapPin className="mt-0.5 h-3 w-3" />
            <span>{address}</span>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <Navigation className="h-3 w-3" />
            <span>
              Lat {location.lat.toFixed(4)}, Lng {location.lng.toFixed(4)}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default SafeSpotCard;
