# =============================================================
# Emlak Platformu - Windows PowerShell Kurulum Scripti
# =============================================================
# Kullanim: .\setup.ps1
# Eger "running scripts is disabled" hatasi alirsaniz,
# once su komutu calistirin:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# =============================================================

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Akilli Emlak Platformu - Kurulum" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Python kontrolu
try {
    $pyVersion = python --version 2>&1
    Write-Host "Python bulundu: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "HATA: Python bulunamadi. Python 3.11+ yukleyip tekrar deneyin." -ForegroundColor Red
    Write-Host "Indirme adresi: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 1) Sanal ortam
if (-not (Test-Path ".venv")) {
    Write-Host ""
    Write-Host "[1/5] Sanal ortam olusturuluyor (.venv)..." -ForegroundColor Cyan
    python -m venv .venv
} else {
    Write-Host "[1/5] Sanal ortam zaten mevcut." -ForegroundColor Yellow
}

# Aktiflestir
& .\.venv\Scripts\Activate.ps1

# 2) pip yukseltme
Write-Host ""
Write-Host "[2/5] pip yukseltiliyor..." -ForegroundColor Cyan
python -m pip install --upgrade pip wheel setuptools

# 3) Python paketleri
Write-Host ""
Write-Host "[3/5] Python bagimliliklari yukleniyor (10-15 dk surebilir)..." -ForegroundColor Cyan
pip install -r requirements.txt

# 4) Playwright
Write-Host ""
Write-Host "[4/5] Playwright tarayicisi indiriliyor..." -ForegroundColor Cyan
try {
    playwright install chromium
} catch {
    Write-Host "Playwright atlandi. Daha sonra 'playwright install' komutunu calistirabilirsiniz." -ForegroundColor Yellow
}

# 5) Frontend
Write-Host ""
if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "[5/5] Frontend bagimliliklari yukleniyor..." -ForegroundColor Cyan
    Push-Location frontend
    npm install
    Pop-Location
} else {
    Write-Host "[5/5] npm bulunamadi - frontend atlandi." -ForegroundColor Yellow
    Write-Host "      Node.js 20+ yukleyip 'cd frontend; npm install' calistirin." -ForegroundColor Yellow
}

# .env kopyala
if ((-not (Test-Path ".env")) -and (Test-Path ".env.example")) {
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host ".env dosyasi .env.example'dan kopyalandi. Degerleri duzenlemeyi unutmayin." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "  Kurulum tamamlandi" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Sonraki adimlar:" -ForegroundColor Cyan
Write-Host "  1) Sanal ortami aktiflestirin  : .\.venv\Scripts\Activate.ps1"
Write-Host "  2) Veritabanini baslatin       : docker-compose up -d postgres mlflow"
Write-Host "  3) Migration calistirin        : cd backend; alembic revision --autogenerate -m 'init'; alembic upgrade head"
Write-Host "  4) Backendi baslatin           : cd backend; uvicorn app.main:app --reload"
Write-Host "  5) Frontendi baslatin          : cd frontend; npm run dev"
Write-Host ""
