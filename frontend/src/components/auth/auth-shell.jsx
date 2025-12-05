import AnimatedWrapper from '../ui/animated-wrapper.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card.jsx';

function AuthShell({ title, description, children }) {
  return (
    <AnimatedWrapper direction="up" delay={0.05} className="w-full max-w-md">
      <Card className="shadow-soft">
        <CardHeader className="space-y-1">
          <CardTitle className="text-lg font-semibold tracking-tight">{title}</CardTitle>
          {description && (
            <CardDescription className="text-xs text-slate-500 dark:text-slate-400">
              {description}
            </CardDescription>
          )}
        </CardHeader>
        <CardContent className="space-y-4">{children}</CardContent>
      </Card>
    </AnimatedWrapper>
  );
}

export default AuthShell;
