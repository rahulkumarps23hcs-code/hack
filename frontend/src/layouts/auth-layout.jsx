import { Outlet } from 'react-router-dom';
import Navbar from '../components/ui/navbar.jsx';
import Footer from '../components/ui/footer.jsx';

function AuthLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-50">
      <Navbar minimal />
      <main className="flex-1 flex items-center justify-center px-4 py-10">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default AuthLayout;
