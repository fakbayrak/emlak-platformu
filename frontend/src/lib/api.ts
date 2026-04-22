import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  timeout: 15_000,
});

// ---- Tip tanımları ----
export interface HouseFeatures {
  city: string;
  district: string;
  neighborhood?: string;
  m2: number;
  room_count: string;
  building_age?: number;
  floor?: number;
  heating_type?: string;
  furnished?: boolean;
  has_elevator?: boolean;
  has_parking?: boolean;
}

export interface SHAPFeature {
  name: string;
  contribution_tl: number;
  direction: "+" | "-";
}

export interface PredictionResponse {
  predicted_price_nominal: number;
  predicted_price_real: number;
  confidence_interval?: [number, number];
  model_version: string;
  top_shap_features: SHAPFeature[];
  currency: string;
}

// ---- API fonksiyonları ----
export const predictSale = (features: HouseFeatures) =>
  api.post<PredictionResponse>("/predict/sale", features).then((r) => r.data);

export const predictRent = (features: HouseFeatures) =>
  api.post<PredictionResponse>("/predict/rent", features).then((r) => r.data);

export const analyzeDeal = (features: HouseFeatures, askingPrice: number) =>
  api.post("/analyze/deal", { features, asking_price: askingPrice }).then((r) => r.data);

export const getDistricts = () =>
  api.get("/analytics/districts").then((r) => r.data);

export const getModelMetrics = () =>
  api.get("/model/metrics").then((r) => r.data);
