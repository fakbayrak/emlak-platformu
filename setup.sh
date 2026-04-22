#!/usr/bin/env bash
# =============================================================
# Emlak Platformu — Tek Komutla Sanal Ortam Kurulumu
# =============================================================
# Kullanım: ./setup.sh
# Windows'ta Git Bash veya WSL altında çalıştırın.
# =============================================================
set -e

echo "======================================"
echo "  Akıllı Emlak Platformu — Kurulum"
echo "======================================"

# Python sürüm kontrolü
if ! command -v python3 &> /dev/null; then
    echo "HATA: python3 bulunamadı. Python 3.11+ yükleyip tekrar deneyin."
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python sürümü: $PY_VERSION"

# 1) Sanal ortam
if [ ! -d ".venv" ]; then
    echo "[1/5] Sanal ortam oluşturuluyor (.venv)..."
    python3 -m venv .venv
else
    echo "[1/5] Sanal ortam zaten mevcut."
fi

# shellcheck disable=SC1091
source .venv/bin/activate

# 2) pip yükseltme
echo "[2/5] pip yükseltiliyor..."
pip install --upgrade pip wheel setuptools

# 3) Python paketleri
echo "[3/5] Python bağımlılıkları yükleniyor (10-15 dk sürebilir)..."
pip install -r requirements.txt

# 4) Playwright Chromium
echo "[4/5] Playwright tarayıcısı indiriliyor..."
playwright install chromium || echo "Not: Playwright şimdilik kurulmadı, sonra 'playwright install' deneyin."

# 5) Frontend
if command -v npm &> /dev/null; then
    echo "[5/5] Frontend bağımlılıkları yükleniyor..."
    ( cd frontend && npm install )
else
    echo "[5/5] npm bulunamadı — frontend'i atlıyorum. Node.js 20+ yükleyip 'cd frontend && npm install' çalıştırın."
fi

# .env kopyala
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo ".env dosyası .env.example'dan kopyalandı. Lütfen değerleri düzenleyin."
fi

echo ""
echo "======================================"
echo "  Kurulum tamamlandı ✓"
echo "======================================"
echo ""
echo "Sonraki adımlar:"
echo "  1) Sanal ortamı aktifleştirin : source .venv/bin/activate"
echo "  2) Veritabanını başlatın      : docker-compose up -d postgres mlflow"
echo "  3) Migration'ları çalıştırın  : cd backend && alembic revision --autogenerate -m 'init' && alembic upgrade head"
echo "  4) Backend'i başlatın         : cd backend && uvicorn app.main:app --reload"
echo "  5) Frontend'i başlatın        : cd frontend && npm run dev"
echo ""
