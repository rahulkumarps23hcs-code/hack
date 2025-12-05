import { cn } from '../../utils/cn.js';

function Button({ variant = 'primary', size = 'md', className = '', disabled, ...rest }) {
  const base = 'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary-500 disabled:opacity-60 disabled:cursor-not-allowed ring-offset-slate-950';
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 shadow-soft',
    outline: 'border border-slate-300/80 dark:border-slate-700/80 bg-transparent hover:bg-slate-100/60 dark:hover:bg-slate-800/60',
    ghost: 'bg-transparent hover:bg-slate-100/60 dark:hover:bg-slate-800/60',
    danger: 'bg-danger-500 text-white hover:bg-red-600 shadow-soft',
    subtle: 'bg-slate-100 text-slate-800 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700',
  };
  const sizes = {
    sm: 'h-8 px-3 text-xs',
    md: 'h-10 px-4 text-sm',
    lg: 'h-11 px-6 text-base',
    icon: 'h-10 w-10',
  };

  return (
    <button
      className={cn(base, variants[variant] ?? variants.primary, sizes[size] ?? sizes.md, className)}
      disabled={disabled}
      {...rest}
    />
  );
}

export default Button;
