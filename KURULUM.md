# Kurulum Kılavuzu

## Ön Koşullar

| Araç | Minimum Sürüm | Kurulum |
|------|---------------|---------|
| Python | 3.11 | [python.org](https://www.python.org/downloads/) |
| Node.js | 20 | [nodejs.org](https://nodejs.org/) |
| Docker | 24+ | [docker.com](https://www.docker.com/products/docker-desktop) |
| Git | 2.40+ | [git-scm.com](https://git-scm.com/) |

## Hızlı Kurulum (Tek Komutla)

### Linux / macOS / WSL

```bash
cd emlak-platformu
./setup.sh
```

### Windows (PowerShell)

```powershell
cd emlak-platformu
.\setup.ps1
```

Bu scriptler:
1. `.venv` adında sanal ortam oluşturur
2. `requirements.txt`'i yükler (backend + ml + scraper paketleri birlikte)
3. Playwright Chromium tarayıcısını indirir
4. Frontend bağımlılıklarını yükler (`npm install`)
5. `.env` dosyasını `.env.example`'dan kopyalar

## Manuel Kurulum

### 1. Python Sanal Ortamı

```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.\.venv\Scripts\activate

pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
playwright install chromium
```

### 2. Frontend

```bash
cd frontend
npm install
cd ..
```

### 3. Ortam Değişkenleri

```bash
cp .env.example .env
# .env dosyasını açıp değerleri kendi ortamınıza göre düzenleyin
```

### 4. Veritabanı ve MLflow

```bash
# Docker ile (önerilen)
docker-compose up -d postgres mlflow

# Servislerin hazır olmasını bekleyin (10-15 sn)
docker-compose ps
```

### 5. Veritabanı Şeması

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
cd ..
```

## Geliştirme Sunucularını Başlatma

Her birini ayrı terminalde çalıştırın:

### Terminal 1 — Backend

```bash
source .venv/bin/activate
cd backend
uvicorn app.main:app --reload --port 8000
```

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

- Arayüz: http://localhost:5173

### Terminal 3 — MLflow UI

```bash
# Docker ile zaten çalışıyor: http://localhost:5000
# Yerel çalıştırmak isterseniz:
source .venv/bin/activate
mlflow server --host 0.0.0.0 --port 5000
```

### Terminal 4 — Scraper (isteğe bağlı)

```bash
source .venv/bin/activate
cd scraper
scrapy crawl sample -o ../ml/data/raw/sample.json
```

## Tüm Servisleri Docker ile Ayağa Kaldırma

```bash
docker-compose up -d
```

Bu komut şunları başlatır:
- PostgreSQL (5432)
- MLflow (5000)
- Backend API (8000)
- Frontend (5173)

## Test Çalıştırma

### Backend

```bash
source .venv/bin/activate
cd backend
pytest --cov=app --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm test           # Vitest birim testleri
npm run e2e        # Playwright E2E testleri (opsiyonel)
```

### Lint ve Format

```bash
# Backend
ruff check backend/app
black --check backend/app

# Frontend
cd frontend
npm run lint
npm run format
```

## Model Eğitimi

```bash
source .venv/bin/activate

# Satılık model
python ml/scripts/train_sale.py

# Kiralık model
python ml/scripts/train_rent.py

# Benzer ilan cache'i
python ml/scripts/build_similarity_cache.py
```

E�itim sonuçları MLflow UI'dan izlenebilir: http://localhost:5000

## Sorun Giderme

### `psycopg2` kurulum hatası (Linux)

```bash
sudo apt install libpq-dev python3-dev
pip install --force-reinstall psycopg2-binary
```

### Windows'ta `shap` veya `xgboost` hatası

Microsoft C++ Build Tools yüklü olmalı:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Port çakışmaları

`.env` dosyasındaki port değerlerini değiştirin veya çakışan servisleri durdurun:

```bash
lsof -i :8000     # Linux/Mac
netstat -ano | findstr 8000   # Windows
```

### Playwright Chromium indirilemiyor

```bash
# Proxy arkasındaysanız:
PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net playwright install chromium
```

## Üretim Dağıtımı (İsteğe Bağlı)

```bash
# docker-compose ile canlıya almak için:
docker-compose -f docker-compose.yml up -d --build

# Railway.app ya da Render gibi platformlar için:
# - backend/Dockerfile'ı kullanın
# - Environment değişkenlerini panel üzerinden girin
```
