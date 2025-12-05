import { Outlet } from 'react-router-dom';
import Navbar from '../components/ui/navbar.jsx';
import Footer from '../components/ui/footer.jsx';

function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-50">
      <Navbar />
      <main className="flex-1 container py-6 sm:py-8 lg:py-10">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default MainLayout;
