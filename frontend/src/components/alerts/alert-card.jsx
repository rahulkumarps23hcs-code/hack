import { AlertTriangle, MapPin, Clock } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card.jsx';
import Badge from '../ui/badge.jsx';

function getSeverityBadgeVariant(severity) {
  switch (severity) {
    case 'high':
      return 'danger';
    case 'medium':
      return 'warning';
    case 'low':
    default:
      return 'success';
  }
}

function getSeverityLabel(severity) {
  switch (severity) {
    case 'high':
      return 'High risk';
    case 'medium':
      return 'Moderate risk';
    case 'low':
    default:
      return 'Low risk';
  }
}

function AlertCard({ alert }) {
  if (!alert) {
    return null;
  }

  const { type, severity, timestamp, location, description } = alert;

  return (
    <Card className="flex flex-col gap-3">
      <CardHeader>
        <div className="flex items-start gap-3">
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-danger-500/10 text-danger-500">
            <AlertTriangle className="h-4 w-4" />
          </span>
          <div className="space-y-1">
            <CardTitle className="flex items-center gap-2">
              <span className="capitalize">{type.replace('-', ' ')}</span>
              <Badge variant={getSeverityBadgeVariant(severity)}>{getSeverityLabel(severity)}</Badge>
            </CardTitle>
            <CardDescription>
              <span className="inline-flex items-center gap-1">
                <Clock className="h-3 w-3" />
                <span>{new Date(timestamp).toLocaleString()}</span>
              </span>
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-xs text-slate-600 dark:text-slate-200">{description}</p>
        <div className="mt-2 inline-flex items-center gap-2 rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          <MapPin className="h-3 w-3" />
          <span>
            Lat {location.lat.toFixed(4)}, Lng {location.lng.toFixed(4)}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}

export default AlertCard;
