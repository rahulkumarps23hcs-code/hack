import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './card.jsx';

function FeatureCard({ icon, title, description, badge }) {
  return (
    <Card className="h-full border-slate-200/70 bg-slate-50/80 dark:border-slate-800/80 dark:bg-slate-950/60">
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-3">
            {icon && (
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-primary-600/10 text-primary-600">
                {icon}
              </span>
            )}
            <div>
              <CardTitle>{title}</CardTitle>
              {badge && (
                <span className="mt-0.5 inline-flex rounded-full bg-primary-600/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">
                  {badge}
                </span>
              )}
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <CardDescription className="text-xs leading-relaxed text-slate-600 dark:text-slate-300">
          {description}
        </CardDescription>
      </CardContent>
    </Card>
  );
}

export default FeatureCard;
