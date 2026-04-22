import { Routes, Route } from "react-router-dom";
import Layout from "@/components/Layout";
import HomePage from "@/pages/HomePage";
import PredictPage from "@/pages/PredictPage";
import DealAnalysisPage from "@/pages/DealAnalysisPage";
import DashboardPage from "@/pages/DashboardPage";
import MapPage from "@/pages/MapPage";
import ModelsPage from "@/pages/ModelsPage";
import ListingsPage from "@/pages/ListingsPage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/predict" element={<PredictPage />} />
        <Route path="/deal" element={<DealAnalysisPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/models" element={<ModelsPage />} />
        <Route path="/listings" element={<ListingsPage />} />
      </Route>
    </Routes>
  );
}
