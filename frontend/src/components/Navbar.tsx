import { NavLink } from "react-router-dom";
import { Home, TrendingUp, Map, LineChart, List, Target } from "lucide-react";

const navItems = [
  { to: "/",          label: "Ana Sayfa",       icon: Home },
  { to: "/predict",   label: "Tahmin",          icon: TrendingUp },
  { to: "/deal",      label: "Fırsat Analizi",  icon: Target },
  { to: "/dashboard", label: "Dashboard",       icon: LineChart },
  { to: "/map",       label: "Harita",          icon: Map },
  { to: "/models",    label: "Modeller",        icon: LineChart },
  { to: "/listings",  label: "İlanlar",         icon: List },
];

export default function Navbar() {
  return (
    <nav className="bg-white border-b sticky top-0 z-10 shadow-sm">
      <div className="container mx-auto px-4 flex items-center gap-6 h-14">
        <span className="font-bold text-brand-700">Emlak Analiz</span>
        <div className="flex gap-1 overflow-x-auto">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to} to={to} end={to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm whitespace-nowrap ${
                  isActive ? "bg-brand-100 text-brand-700" : "text-gray-600 hover:bg-gray-100"
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}
