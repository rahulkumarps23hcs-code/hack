import { cn } from '../../utils/cn.js';

function LoadingSkeleton({ className = '' }) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-slate-200/80 dark:bg-slate-800/80', className)}
    />
  );
}

export default LoadingSkeleton;
