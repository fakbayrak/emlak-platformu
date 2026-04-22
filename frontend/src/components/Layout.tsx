import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <footer className="py-6 text-center text-sm text-gray-500 border-t bg-white">
        © 2026 Akıllı Emlak Tahmin Platformu — Bitirme Projesi
      </footer>
    </div>
  );
}
