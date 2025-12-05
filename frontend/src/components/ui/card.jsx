import { cn } from '../../utils/cn.js';

function Card({ className = '', ...rest }) {
  return (
    <div
      className={cn(
        'rounded-xl border border-slate-200/70 bg-white/90 p-4 shadow-sm dark:border-slate-800/80 dark:bg-slate-900/90',
        className
      )}
      {...rest}
    />
  );
}

function CardHeader({ className = '', ...rest }) {
  return <div className={cn('mb-3 flex items-start justify-between gap-2', className)} {...rest} />;
}

function CardTitle({ className = '', ...rest }) {
  return <h3 className={cn('text-sm font-semibold tracking-tight', className)} {...rest} />;
}

function CardDescription({ className = '', ...rest }) {
  return <p className={cn('text-xs text-slate-500 dark:text-slate-400', className)} {...rest} />;
}

function CardContent({ className = '', ...rest }) {
  return <div className={cn('space-y-3 text-sm', className)} {...rest} />;
}

export { Card, CardHeader, CardTitle, CardDescription, CardContent };
