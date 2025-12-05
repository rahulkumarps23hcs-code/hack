import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { Shield, Bell, Map, Moon, Sun, Menu, X } from 'lucide-react';
import Button from './button.jsx';
import { useTheme } from '../../context/theme-context.jsx';
import { useAuth } from '../../context/auth-context.jsx';
import { cn } from '../../utils/cn.js';

function Navbar({ minimal = false }) {
  const { theme, toggleTheme } = useTheme();
  const { user, isAuthenticated, logout } = useAuth();
  const [open, setOpen] = useState(false);

  const links = [
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/alerts', label: 'Alerts' },
    { to: '/map', label: 'Map' },
    { to: '/safe-spots', label: 'Safe Spots' },
    { to: '/sos', label: 'SOS' },
  ];

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="border-b border-slate-200/70 bg-white/80 backdrop-blur-md dark:border-slate-800/80 dark:bg-slate-950/80">
      <nav className="container flex h-16 items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-2">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-primary-600 text-white shadow-soft">
              <Shield className="h-4 w-4" />
            </span>
            <span className="flex flex-col leading-tight">
              <span className="text-sm font-semibold tracking-tight">Safe-Zone</span>
              <span className="text-[11px] font-medium uppercase text-slate-500 dark:text-slate-400">
                Safety Intelligence
              </span>
            </span>
          </Link>
        </div>

        {!minimal && (
          <>
            <div className="hidden items-center gap-6 md:flex">
              {links.map((link) => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) =>
                    cn(
                      'text-sm font-medium text-slate-600 transition-colors hover:text-slate-900 dark:text-slate-300 dark:hover:text-white',
                      isActive && 'text-primary-600 dark:text-primary-400'
                    )
                  }
                >
                  {link.label}
                </NavLink>
              ))}
            </div>

            <div className="hidden items-center gap-2 md:flex">
              <button
                type="button"
                onClick={toggleTheme}
                className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-200/80 bg-slate-50 text-slate-700 shadow-sm hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
              >
                {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </button>

              {isAuthenticated ? (
                <>
                  <div className="flex items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700 dark:bg-slate-900/70 dark:text-slate-200">
                    <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-primary-600/90 text-[10px] font-semibold text-white">
                      {user?.name?.[0]?.toUpperCase() ?? 'U'}
                    </span>
                    <span className="max-w-[120px] truncate">{user?.name ?? 'User'}</span>
                  </div>
                  <Button variant="outline" size="sm" onClick={handleLogout}>
                    Logout
                  </Button>
                </>
              ) : (
                <div className="flex items-center gap-2">
                  <Link to="/login">
                    <Button variant="ghost" size="sm" className="px-2 text-xs">
                      Sign in
                    </Button>
                  </Link>
                  <Link to="/signup">
                    <Button size="sm" className="text-xs">
                      Get Started
                    </Button>
                  </Link>
                </div>
              )}

              <button
                type="button"
                className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-200/80 bg-slate-50 text-slate-700 shadow-sm hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
                aria-label="Notifications"
              >
                <Bell className="h-4 w-4" />
              </button>
            </div>

            <button
              type="button"
              className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-200/80 bg-slate-50 text-slate-700 shadow-sm hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800 md:hidden"
              onClick={() => setOpen((prev) => !prev)}
              aria-label="Toggle navigation"
            >
              {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
            </button>
          </>
        )}
      </nav>

      {!minimal && open && (
        <div className="border-t border-slate-200/70 bg-white/95 py-3 shadow-sm dark:border-slate-800/80 dark:bg-slate-950/95 md:hidden">
          <div className="container flex flex-col gap-3">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  cn(
                    'text-sm font-medium text-slate-700 hover:text-primary-600 dark:text-slate-200 dark:hover:text-primary-400',
                    isActive && 'text-primary-600 dark:text-primary-400'
                  )
                }
              >
                {link.label}
              </NavLink>
            ))}

            <div className="mt-2 flex items-center justify-between gap-3">
              <button
                type="button"
                onClick={toggleTheme}
                className="inline-flex h-9 w-9 items-center justify-center rounded-full border border-slate-200/80 bg-slate-50 text-slate-700 shadow-sm hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
              >
                {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </button>

              {isAuthenticated ? (
                <Button variant="outline" size="sm" className="flex-1" onClick={handleLogout}>
                  Logout
                </Button>
              ) : (
                <div className="flex flex-1 items-center justify-end gap-2">
                  <Link to="/login" onClick={() => setOpen(false)}>
                    <Button variant="ghost" size="sm">
                      Sign in
                    </Button>
                  </Link>
                  <Link to="/signup" onClick={() => setOpen(false)}>
                    <Button size="sm">Get Started</Button>
                  </Link>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2 text-[11px] text-slate-500 dark:text-slate-400">
              <Map className="h-3 w-3" />
              <span>AI-ready real-time safety intelligence</span>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

export default Navbar;
