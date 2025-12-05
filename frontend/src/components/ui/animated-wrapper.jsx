import { motion } from 'framer-motion';
import { cn } from '../../utils/cn.js';

function getOffset(direction) {
  switch (direction) {
    case 'up':
      return { y: 12 };
    case 'down':
      return { y: -12 };
    case 'left':
      return { x: 16 };
    case 'right':
      return { x: -16 };
    default:
      return { y: 12 };
  }
}

function AnimatedWrapper({ children, className = '', delay = 0, direction = 'up' }) {
  const offset = getOffset(direction);

  return (
    <motion.div
      className={cn(className)}
      initial={{ opacity: 0, ...offset }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut', delay }}
    >
      {children}
    </motion.div>
  );
}

export default AnimatedWrapper;
