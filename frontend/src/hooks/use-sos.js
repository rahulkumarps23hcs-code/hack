import { useCallback, useMemo, useState } from 'react';

export function useSos() {
  const [isListeningVoice, setIsListeningVoice] = useState(true);
  const [isListeningShake, setIsListeningShake] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const [lastTriggeredAt, setLastTriggeredAt] = useState(null);
  const [lastTriggerSource, setLastTriggerSource] = useState(null);

  const trigger = useCallback((source = 'button') => {
    const timestamp = new Date().toISOString();
    setIsActive(true);
    setLastTriggeredAt(timestamp);
    setLastTriggerSource(source);
  }, []);

  const reset = useCallback(() => {
    setIsActive(false);
  }, []);

  const statusLabel = useMemo(() => {
    if (isActive) {
      return 'SOS active - location would be shared with trusted contacts';
    }
    if (isListeningVoice || isListeningShake) {
      return 'Listening for voice or shake triggers (dummy mode).';
    }
    return 'SOS is on standby.';
  }, [isActive, isListeningShake, isListeningVoice]);

  return {
    isListeningVoice,
    isListeningShake,
    isActive,
    lastTriggeredAt,
    lastTriggerSource,
    setIsListeningVoice,
    setIsListeningShake,
    trigger,
    reset,
    statusLabel,
  };
}
