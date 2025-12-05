import { cn } from '../../utils/cn.js';

function InputField({
  id,
  label,
  type = 'text',
  helperText,
  error,
  className = '',
  inputClassName = '',
  ...rest
}) {
  return (
    <div className={cn('space-y-1.5', className)}>
      {label && (
        <label
          htmlFor={id}
          className="block text-xs font-medium text-slate-600 dark:text-slate-300"
        >
          {label}
        </label>
      )}
      <input
        id={id}
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-slate-300/80 bg-white/90 px-3 py-2 text-sm text-slate-900 shadow-sm transition-colors placeholder:text-slate-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-700/80 dark:bg-slate-900/80 dark:text-slate-50',
          error && 'border-danger-500 focus-visible:ring-danger-500',
          inputClassName
        )}
        {...rest}
      />
      {helperText && !error && (
        <p className="text-[11px] text-slate-500 dark:text-slate-400">{helperText}</p>
      )}
      {error && <p className="text-[11px] text-danger-500">{error}</p>}
    </div>
  );
}

export default InputField;
