# Akıllı Emlak Fiyat Tahmin ve Analiz Platformu

> Bitirme Projesi — Faruk Akbayrak (232923077)
> Danışman: Ahmet Haşim Yurttakal
> Bölüm: Bilgisayar Mühendisliği

Türkiye konut piyasası için makine öğrenmesi tabanlı fiyat tahmin, fırsat analizi ve yatırım skorlama platformu.

## 🏗️ Proje Yapısı

```
emlak-platformu/
├── backend/          # FastAPI REST API
├── ml/               # Makine öğrenmesi kodu, modeller, notebook'lar
├── scraper/          # Scrapy + Playwright web scraper
├── frontend/         # React + TypeScript + Tailwind + shadcn/ui
├── docs/             # Proje dokümantasyonu
├── .github/workflows # CI/CD pipeline'ları
├── docker-compose.yml
└── README.md
```

## 🧰 Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| Veri Toplama | Python 3.11, Scrapy, Playwright, BeautifulSoup4 |
| Veri Katmanı | PostgreSQL 15, SQLAlchemy, Alembic, pandas |
| ML | scikit-learn, XGBoost, LightGBM, SHAP, MLflow |
| API | FastAPI, Pydantic, Uvicorn |
| Frontend | React 18, Vite, TypeScript, Tailwind, shadcn/ui, Leaflet.js, Chart.js |
| Test | pytest, httpx, Vitest, Playwright |
| DevOps | Docker, docker-compose, GitHub Actions |

## 📦 Yedi Ana Modül

| Modül | Açıklama |
|-------|----------|
| M1 — Satılık Tahmin | Konut özelliklerine göre satış fiyatı tahmini + SHAP açıklaması |
| M2 — Kiralık Tahmin | Konut özelliklerine göre aylık kira tahmini + SHAP |
| M3 — Fırsat Analizi | Gerçek fiyat vs tahmin: Fırsat / Uygun / Pahalı etiketleme |
| M4 — Yatırım Dashboard | İlçe bazlı 0-100 yatırım skoru (5 bileşen) |
| M5 — Harita | Leaflet.js interaktif choropleth harita |
| M6 — Benzer İlan | Cosine similarity tabanlı öneri sistemi |
| M7 — Model Karşılaştırma | MAE/RMSE/R²/MAPE panel |

## 🚀 Hızlı Başlangıç

### Ön Koşullar

- Python 3.11+
- Node.js 20+
- Docker & docker-compose
- Git

### 1. Klonlama ve Ortam Kurulumu

```bash
git clone <repo-url>
cd emlak-platformu

# Python sanal ortamı
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .\.venv\Scripts\activate     # Windows

# Tüm Python bağımlılıkları
pip install -r requirements.txt

# Frontend bağımlılıkları
cd frontend && npm install && cd ..
```

### 2. Ortam Değişkenleri

```bash
cp .env.example .env
# .env dosyasını düzenleyip değerleri doldurun
```

### 3. Docker ile Tüm Servisleri Ayağa Kaldırma

```bash
docker-compose up -d
```

Servisler:
- PostgreSQL → `localhost:5432`
- MLflow UI → `http://localhost:5000`
- Backend API → `http://localhost:8000` (dokümantasyon: `/docs`)
- Frontend → `http://localhost:5173`

### 4. İlk Kurulum Komutları

```bash
# Veritabanı migration'ı
cd backend && alembic upgrade head

# Scraping (örnek)
cd scraper && scrapy crawl sample -o ../ml/data/raw/sample.json

# Model eğitimi
cd ml && python scripts/train_sale.py
cd ml && python scripts/train_rent.py
```

## 🧪 Test

```bash
# Backend
cd backend && pytest --cov=app --cov-report=term-missing

# Frontend
cd frontend && npm test

# E2E
cd frontend && npx playwright test
```

## 📊 Yatırım Skoru Formülü

```
investment_score = 100 × (0.30 × yield
                        + 0.25 × appreciation
                        + 0.20 × stability
                        + 0.15 × liquidity
                        + 0.10 × affordability)
```

Ayrıntılar: [docs/01_proje_oneri_v2.docx](docs/01_proje_oneri_v2.docx)

## 📅 Çalışma Planı

30 haftalık detaylı plan: [docs/02_haftalik_plan.docx](docs/02_haftalik_plan.docx)

## 🤝 Katkı

Bu bir bitirme projesidir. Geri bildirim ve öneri için issue açabilirsiniz.

## 📄 Lisans

MIT License (akademik amaçlı)
