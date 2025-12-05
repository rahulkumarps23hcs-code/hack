import { motion } from 'framer-motion';
import { Siren } from 'lucide-react';
import Button from '../ui/button.jsx';

function SosButton({ isActive, onTrigger }) {
  return (
    <motion.div
      className="relative flex items-center justify-center"
      initial={false}
      animate={isActive ? { scale: 1.02 } : { scale: 1 }}
      transition={{ type: 'spring', stiffness: 220, damping: 16 }}
    >
      {isActive && (
        <motion.div
          className="absolute h-40 w-40 rounded-full bg-danger-500/20"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 0, scale: 1.5 }}
          transition={{ duration: 1.2, repeat: Infinity, ease: 'easeOut' }}
        />
      )}
      <Button
        type="button"
        size="lg"
        variant="danger"
        className="relative z-10 h-28 w-28 rounded-full text-lg font-semibold shadow-soft"
        onClick={onTrigger}
      >
        <div className="flex flex-col items-center gap-1">
          <Siren className="h-6 w-6" />
          <span>SOS</span>
        </div>
      </Button>
    </motion.div>
  );
}

export default SosButton;
