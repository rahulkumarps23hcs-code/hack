import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus, Phone } from 'lucide-react';
import AuthShell from '../components/auth/auth-shell.jsx';
import InputField from '../components/ui/input-field.jsx';
import Button from '../components/ui/button.jsx';
import AnimatedWrapper from '../components/ui/animated-wrapper.jsx';
import { useAuth } from '../context/auth-context.jsx';
import { useToast } from '../context/toast-context.jsx';

function Signup() {
  const { signup } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const [form, setForm] = useState({ name: '', email: '', phone: '', password: '' });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validate = () => {
    const nextErrors = {};
    if (!form.name) {
      nextErrors.name = 'Name is required';
    }
    if (!form.email) {
      nextErrors.email = 'Email is required';
    }
    if (!form.phone) {
      nextErrors.phone = 'Phone is required';
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
      await signup(form);
      addToast({
        variant: 'success',
        title: 'Account created (demo)',
        description: 'You are now signed in to the Safe-Zone demo environment.',
      });
      navigate('/dashboard', { replace: true });
    } catch (error) {
      addToast({
        variant: 'error',
        title: 'Signup failed',
        description: 'Demo signup failed. Please try again.',
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthShell
      title="Create your Safe-Zone account"
      description="Set up a demo profile to explore the full safety dashboard and SOS flows."
    >
      <form className="space-y-4" onSubmit={handleSubmit} noValidate>
        <InputField
          id="name"
          name="name"
          label="Full name"
          value={form.name}
          onChange={handleChange}
          error={errors.name}
        />
        <InputField
          id="email"
          name="email"
          type="email"
          label="Email"
          value={form.email}
          onChange={handleChange}
          autoComplete="email"
          error={errors.email}
        />
        <InputField
          id="phone"
          name="phone"
          label="Phone"
          value={form.phone}
          onChange={handleChange}
          autoComplete="tel"
          helperText="Use a sample number, this is not sent anywhere."
          error={errors.phone}
        />
        <InputField
          id="password"
          name="password"
          type="password"
          label="Password"
          value={form.password}
          onChange={handleChange}
          autoComplete="new-password"
          error={errors.password}
        />
        <Button type="submit" className="w-full" disabled={submitting}>
          {submitting ? 'Creating account…' : 'Create account'}
        </Button>
      </form>
      <AnimatedWrapper direction="up" delay={0.08} className="mt-3 text-[11px] text-slate-500">
        <div className="flex items-center gap-1 text-[11px]">
          <UserPlus className="h-3 w-3" />
          <span>
            Already have an account?{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:underline dark:text-primary-400">
              Sign in
            </Link>
          </span>
        </div>
        <div className="mt-2 inline-flex items-center gap-1 text-[11px] text-slate-500">
          <Phone className="h-3 w-3" />
          <span>Demo only: phone and password are kept in local storage.</span>
        </div>
      </AnimatedWrapper>
    </AuthShell>
  );
}

export default Signup;
