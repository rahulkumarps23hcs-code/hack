import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Lock, Mail } from 'lucide-react';
import AuthShell from '../components/auth/auth-shell.jsx';
import InputField from '../components/ui/input-field.jsx';
import Button from '../components/ui/button.jsx';
import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import { useAuth } from '../context/auth-context.jsx';
import { useToast } from '../context/toast-context.jsx';

function Login() {
  const { login } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const [form, setForm] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validate = () => {
    const nextErrors = {};
    if (!form.email) {
      nextErrors.email = 'Email is required';
    }
    if (!form.password) {
      nextErrors.password = 'Password is required';
    } else if (form.password.length < 6) {
      nextErrors.password = 'Password must be at least 6 characters';
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validate()) {
      return;
    }
    setSubmitting(true);
    try {
      await login({ email: form.email, password: form.password });
      addToast({
        variant: 'success',
        title: 'Logged in (demo)',
        description: 'You are now authenticated in the Safe-Zone demo environment.',
      });
      navigate('/dashboard', { replace: true });
    } catch (error) {
      addToast({
        variant: 'error',
        title: 'Login failed',
        description: 'Demo login failed. Please try again.',
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthShell
      title="Welcome back"
      description="Log in to access your personal safety dashboard and alerts. This is a demo-only frontend."
    >
      <form className="space-y-4" onSubmit={handleSubmit} noValidate>
        <InputField
          id="email"
          name="email"
          type="email"
          label="Email"
          value={form.email}
          onChange={handleChange}
          autoComplete="email"
          error={errors.email}
          helperText="Use any valid email to explore the demo."
        />
        <InputField
          id="password"
          name="password"
          type="password"
          label="Password"
          value={form.password}
          onChange={handleChange}
          autoComplete="current-password"
          error={errors.password}
          helperText="Minimum 6 characters. No real authentication is performed."
        />
        <Button type="submit" className="w-full" disabled={submitting}>
          {submitting ? 'Signing in…' : 'Sign in'}
        </Button>
      </form>
      <AnimatedWrapper direction="up" delay={0.08} className="mt-3 text-[11px] text-slate-500">
        <div className="flex items-center justify-between">
          <span className="inline-flex items-center gap-1">
            <Mail className="h-3 w-3" />
            <span>Demo only, no data is sent to a server.</span>
          </span>
        </div>
        <div className="mt-2 flex items-center gap-1 text-[11px]">
          <Lock className="h-3 w-3" />
          <span>
            New here?{' '}
            <Link to="/signup" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              Create a demo account
            </Link>
          </span>
        </div>
      </AnimatedWrapper>
    </AuthShell>
  );
}

export default Login;
