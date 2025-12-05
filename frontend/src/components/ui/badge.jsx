import { cn } from '../../utils/cn.js';

function Badge({ variant = 'default', className = '', ...rest }) {
  const variants = {
    default: 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-100',
    success: 'bg-green-100 text-green-800 dark:bg-green-900/60 dark:text-green-200',
    danger: 'bg-red-100 text-red-800 dark:bg-red-900/60 dark:text-red-200',
    warning: 'bg-amber-100 text-amber-800 dark:bg-amber-900/60 dark:text-amber-200',
    outline:
      'border border-slate-200 text-slate-700 dark:border-slate-700 dark:text-slate-200 bg-transparent',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-wide',
        variants[variant] ?? variants.default,
        className
      )}
      {...rest}
    />
  );
}

export default Badge;
