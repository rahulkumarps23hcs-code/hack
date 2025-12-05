import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card.jsx';
import SosButton from '../components/sos/sos-button.jsx';
import Button from '../components/ui/button.jsx';
import { Mic, Smartphone, Activity, Info } from 'lucide-react';
import { useSos } from '../hooks/use-sos.js';
import { useToast } from '../context/toast-context.jsx';

function SOS() {
  const {
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
  } = useSos();

  const { addToast } = useToast();

  const handleTrigger = (source) => {
    trigger(source);
    addToast({
      variant: 'warning',
      title: 'SOS triggered (demo)',
      description:
        'In production, this would call POST /sos/trigger and notify security + trusted contacts.',
    });
  };

  const handleReset = () => {
    reset();
    addToast({
      variant: 'info',
      title: 'SOS reset',
      description: 'SOS state cleared locally. No external calls were made.',
    });
  };

  return (
    <div className="space-y-6">
      <AnimatedWrapper>
        <div className="space-y-1">
          <h1 className="text-xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">
            SOS centre
          </h1>
          <p className="text-xs text-slate-600 dark:text-slate-300">
            Voice, shake and tap-based SOS triggers. This screen manipulates only local state and is
            wired for future POST /sos/trigger integration.
          </p>
        </div>
      </AnimatedWrapper>

      <div className="grid gap-4 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
        <AnimatedWrapper direction="up" delay={0.02}>
          <Card className="flex flex-col items-center justify-center gap-6 py-8">
            <CardHeader className="text-center">
              <CardTitle>Primary SOS button</CardTitle>
              <CardDescription>
                Tap to simulate an SOS event. In production this would share live location.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-6">
              <SosButton isActive={isActive} onTrigger={() => handleTrigger('button')} />
              <div className="flex flex-wrap items-center justify-center gap-2 text-[11px] text-slate-500 dark:text-slate-400">
                <Activity className="h-3 w-3" />
                <span>{statusLabel}</span>
              </div>
              {lastTriggeredAt && (
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  Last triggered via <span className="font-medium">{lastTriggerSource}</span> at{' '}
                  {new Date(lastTriggeredAt).toLocaleString()}.
                </p>
              )}
              {isActive && (
                <Button variant="outline" size="sm" onClick={handleReset}>
                  Reset SOS state
                </Button>
              )}
            </CardContent>
          </Card>
        </AnimatedWrapper>

        <AnimatedWrapper direction="left" delay={0.06}>
          <Card className="space-y-3">
            <CardHeader>
              <CardTitle>Voice & shake triggers</CardTitle>
              <CardDescription>
                Toggle dummy listeners that represent mobile voice and motion detection.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-xs text-slate-600 dark:text-slate-200">
              <div className="flex items-center justify-between gap-2 rounded-xl bg-slate-100 px-3 py-2 dark:bg-slate-900">
                <div className="flex items-center gap-2">
                  <Mic className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                  <span>Voice keyword: "Safe-Zone help"</span>
                </div>
                <Button
                  size="sm"
                  variant={isListeningVoice ? 'primary' : 'outline'}
                  onClick={() => setIsListeningVoice((prev) => !prev)}
                >
                  {isListeningVoice ? 'Listening' : 'Off'}
                </Button>
              </div>
              <div className="flex items-center justify-between gap-2 rounded-xl bg-slate-100 px-3 py-2 dark:bg-slate-900">
                <div className="flex items-center gap-2">
                  <Smartphone className="h-4 w-4 text-amber-500" />
                  <span>Shake detection</span>
                </div>
                <Button
                  size="sm"
                  variant={isListeningShake ? 'primary' : 'outline'}
                  onClick={() => setIsListeningShake((prev) => !prev)}
                >
                  {isListeningShake ? 'Listening' : 'Off'}
                </Button>
              </div>
              <div className="mt-2 flex items-start gap-2 text-[11px] text-slate-500 dark:text-slate-400">
                <Info className="mt-0.5 h-3 w-3" />
                <p>
                  In a native mobile app, these toggles would bind to the microphone and accelerometer
                  APIs. Here they only modify local state to demonstrate the UX.
                </p>
              </div>
            </CardContent>
          </Card>
        </AnimatedWrapper>
      </div>
    </div>
  );
}

export default SOS;
