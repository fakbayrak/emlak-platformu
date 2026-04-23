# Sohbet Özeti — Hafta 1 Sonu

**Tarih:** 22 Nisan 2026
**Hazırlayan:** Claude (Faruk Akbayrak ile danışmanlık sohbeti sonu)
**Amaç:** Bu belge, Hafta 1 sonunda alınan tüm kararların ve bulguların kalıcı kaydıdır. Yeni bir sohbette devam ederken context köprüsü görevi görür.

---

## 1. Proje Özeti (Bağlam)

**Proje:** Akıllı Emlak Fiyat Tahmin ve Analiz Platformu
**Öğrenci:** Faruk Akbayrak (232923077)
**Üniversite:** Afyon Kocatepe Üniversitesi, Bilgisayar Mühendisliği
**Danışman:** Ahmet Haşim Yurttakal
**GitHub:** [fakbayrak/emlak-platformu](https://github.com/fakbayrak/emlak-platformu) (private)
**Süre:** 30 hafta (Nisan 2026 – Kasım 2026)

### 7 Modül

1. M1 — Satılık fiyat tahmini
2. M2 — Kiralık fiyat tahmini
3. M3 — Fırsat/uygun/pahalı ilan analizi
4. M4 — İlçe bazlı yatırım dashboard
5. M5 — Leaflet.js interaktif harita
6. M6 — Cosine similarity benzer ilan öneri
7. M7 — Model karşılaştırma paneli

### Teknoloji Yığını

- **Backend:** FastAPI + Pydantic + SQLAlchemy + Alembic
- **Veritabanı:** PostgreSQL 15 (Docker)
- **ML:** scikit-learn, XGBoost, LightGBM, SHAP
- **MLOps:** MLflow (Docker, port 5000)
- **Scraping:** Scrapy (Playwright gereksiz — aşağıda açıklandı)
- **Frontend:** React 18 + Vite + TypeScript + Tailwind + shadcn/ui
- **DevOps:** Docker Compose + GitHub Actions CI/CD

### Yatırım Skoru Formülü

```
Skor = 100 × (
  0.30 × yield           (kira verimi)
+ 0.25 × appreciation    (değer artışı)
+ 0.20 × stability       (fiyat istikrarı)
+ 0.15 × liquidity       (likidite)
+ 0.10 × affordability   (erişilebilirlik)
)
```

---

## 2. Hafta 1'de Tamamlananlar

### 2.1 Akademik Belgeler

- [x] **`01_proje_oneri_v2.docx`** — Güncellenmiş proje öneri raporu
  - Web scraping altyapısı + etik çerçeve + Plan B (Kaggle)
  - Enflasyon düzeltmesi (TÜİK KFE, referans ay 2025-01)
  - Yatırım skoru formülü + 5 bileşen tablosu
  - Risk analizi tablosu (7 madde)
  - Test stratejisi (pytest + Playwright + Vitest)
  - MLflow entegrasyonu

- [x] **`02_haftalik_plan.docx`** — 30 haftalık detaylı plan
  - 5 aşama, 11 milestone (M-0 → M-10)
  - Gantt özeti

### 2.2 Teknik Altyapı

- [x] **Monorepo iskeleti** (`emlak-platformu/`)
  - `backend/` — FastAPI, 11 endpoint, 7 SQLAlchemy tablosu, 5 pytest
  - `ml/` — data/features/models/evaluation/scoring/recommender + 3 training script + 5 Jupyter notebook
  - `scraper/` — Scrapy projesi (base_spider + sample_spider placeholder)
  - `frontend/` — React + Vite + TypeScript + Tailwind (7 sayfa)
  - `.github/workflows/` — backend-ci + frontend-ci + model-ci (tümü yeşil ✅)
  - `docs/` — proje dokümantasyonu
  - `docker-compose.yml`

- [x] **Kurulum doğrulandı**
  - Python 3.11, Node.js 24 LTS
  - PostgreSQL + MLflow Docker container'ları çalışıyor
  - FastAPI backend (port 8000) — `/docs` Swagger UI aktif
  - React frontend (port 5173) — 7 sayfa navigasyonu çalışıyor
  - Alembic migration başarılı: 7 tablo + 4 indeks oluşturuldu

- [x] **Git + GitHub**
  - Repo oluşturuldu, initial commit yapıldı
  - Ruff + Black konfigürasyonu yapıldı
  - 3 CI workflow yeşil ✅

### 2.3 Veritabanı Şeması (7 tablo)

```
listings              (ilan ana tablosu)
price_history         (fiyat değişim geçmişi)
economic_indicators   (TÜFE/KFE ayda bir snapshot)
predictions           (model tahminleri logu)
district_stats        (ilçe bazlı özet istatistik)
model_metrics         (model performans takip)
similar_cache         (cosine similarity ön hesap)
```

### 2.4 API Endpoint'leri (11 adet)

```
GET  /health
POST /predict/sale
POST /predict/rent
POST /analyze/deal
GET  /analytics/districts
GET  /analytics/district/{name}
GET  /listings
POST /listings
GET  /listings/{id}
GET  /listings/similar/{id}
GET  /model/metrics
```

---

## 3. Veri Kaynağı Kararı — Emlakjet.com ✅

### 3.1 Aday Siteler ve Değerlendirme

| Site | Durum | Notlar |
|------|-------|--------|
| Sahibinden.com | ❌ ELENDİ | robots.txt /ilan/emlak*/detay yasak; Cloudflare + CAPTCHA; AI botları yasak |
| Hepsiemlak.com | ✅ Aday | robots.txt dostane; ilan detayları serbest |
| Zingat.com | ➖ Gereksiz | Hepsiemlak'la aynı şirket, ayrı değerlendirme gereksiz |
| **Emlakjet.com** | ✅✅✅ **SEÇİLDİ** | En dostane site, teknik olarak ideal |

### 3.2 Emlakjet Neden Seçildi?

**Etik/Hukuki:**
- robots.txt'de `/ilan/...` path'i için yasak yok
- AI botları özel yasaklı değil (sadece Scrappy, discobot, dotbot, yacybot, MJ12 yasak)
- Filtre URL'leri yasaklı ama bizim scraping mantığımızı etkilemiyor

**Teknik (KRİTİK):**
- Sayfa **statik HTML** olarak render oluyor, JavaScript gerekmiyor
- **Playwright GEREKSİZ**, Scrapy yeterli
- Veri 3 farklı yerde bulunuyor (aşağıda açıklandı)

### 3.3 Test Edilen URL

```
https://www.emlakjet.com/ilan/balikesir-altieylul-hasanbasricantay-mh-satilik-31-daire-18816293
```

- Cloudflare/CAPTCHA yok
- Sayfa normal yükleniyor
- Ctrl+U ile kaynak incelendi, tüm veriler düz HTML'de mevcut

---

## 4. Emlakjet Scraping Stratejisi (3 Katmanlı)

### 4.1 Katman 1: JSON-LD Schema.org (PRİMER)

Her ilan sayfasında `<script type="application/ld+json">` içinde standart Product schema bulunuyor:

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "BALIKESİR ALTIEYLÜL HASANBASRİÇANTAY MH SATILIK 3+1 DAİRE",
  "image": "...",
  "description": "Rookz Balşehir ... 125 m² 3+1 Krediye Uygun 0 (Yeni) Satılık Daire 6900000 TL",
  "url": "...",
  "brand": {
    "@type": "Brand",
    "name": "ROOKZ BALŞEHİR GAYRİMENKUL",
    "logo": "..."
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "TRY",
    "price": "6900000",
    "availability": "inStock",
    "priceValidUntil": "2026-12-31",
    "seller": {
      "@type": "RealEstateAgent",
      "telephone": "+908502187997",
      "address": "Balıkesir, Altıeylül"
    }
  }
}
```

**Ek olarak BreadcrumbList** şeması il/ilçe/mahalle hiyerarşisi sağlıyor.

**Kod yaklaşımı:**
```python
json_ld_blocks = response.css('script[type="application/ld+json"]::text').getall()
for block in json_ld_blocks:
    data = json.loads(block)
    if data.get("@type") == "Product":
        # price, title, seller vb. buradan çıkarılır
```

### 4.2 Katman 2: Google Tag Manager dataLayer (META VERİ)

Sayfanın başında `window.dataLayer.push({...})` ile birçok metadata bulunuyor:

```javascript
window.dataLayer.push({
  "item_id": "18816293",
  "ilan_firsat": "no",
  "ilan_yayinlanma_tarihi": "2026-01-12 16:26:27",
  "property_status": "satilik",
  "property_category": "konut",
  "property_subcategory": "daire",
  "city": "balikesir",
  "town": "altieylul",
  "neighborhood": "hasan-basri-cantay-mahallesi",
  "district": "merkez",
  "ilan_fiyat": "6900000",
  "ilan_fiyat_dusen": "no",
  "oda_sayisi": "3+1",
  "foto_adet": "39",
  "ilan_uye_id": "1291499",
  "ilan_uye_tip": "kurumsal"
})
```

**Kod yaklaşımı:**
```python
import re, json
script_text = response.xpath(
    '//script[contains(text(), "dataLayer.push")]/text()'
).get()
match = re.search(r'dataLayer\.push\((\{.*?\})\)', script_text, re.DOTALL)
if match:
    metadata = json.loads(match.group(1))
```

### 4.3 Katman 3: Next.js Hydration Data (BONUS — Endeksa + Demografik)

Sayfada `self.__next_f.push([...])` çağrıları içinde **`pageResponse`** bulunuyor. Bu JSON şunları içeriyor:

**Endeksa Fiyat Analizi:**
- `endeksaValuation.minPrice` — Tahmini min fiyat (örn: 4.900.000 TL)
- `endeksaValuation.maxPrice` — Tahmini max fiyat (örn: 5.600.000 TL)

**Bölge Raporu (districtReportPriceInfos):**
- `averagePriceForSale` — Mahalle ortalaması (örn: 4.945.875 TL)
- `averagePriceForRent` — Ortalama kira (örn: 22.875 TL)
- `amortization` — Geri dönüş süresi (örn: 18 yıl)
- `exchangeRatio` — 1 yıllık değer değişimi (örn: %14)
- `graphics` — 1, 2, 3 yıllık aylık fiyat trendleri + 1 yıl sonrası tahmin

**Demografik Veri (districtReportDemographicInfos):**
- Toplam nüfus, nüfus yoğunluğu
- Eğitim düzeyi dağılımı
- Medeni durum dağılımı
- SES (sosyoekonomik statü) dağılımı
- Yaş grupları dağılımı
- Ortalama hane geliri

**Fiyat Geçmişi (priceHistories):**
```json
[{"price": 6900000, "trend": null, "currency": "TRY", "changedAt": "2026-01-12T16:26:27Z"}]
```

**Benzer İlanlar (similarData):**
- Aynı firmanın diğer ilanları (6 adet)

**Önerilen İlanlar (suggestedListingsData):**
- "Bu ilana bakanlar bunlara da baktı" (10 adet)

**Kod yaklaşımı:**
```python
hydration_scripts = response.xpath(
    '//script[contains(text(), "self.__next_f.push")]/text()'
).getall()
# Regex ile pageResponse JSON'unu çıkar
# Sonra json.loads ile parse et
```

### 4.4 Scraping Stratejisi Özeti

| Veri | Nereden | Öncelik |
|------|---------|---------|
| Fiyat, m², oda sayısı | JSON-LD + dataLayer | PRİMER |
| Konum hiyerarşisi | BreadcrumbList + dataLayer | PRİMER |
| Firma bilgisi | JSON-LD brand/seller | PRİMER |
| Yayın tarihi | dataLayer | PRİMER |
| Endeksa değerleme | Next.js hydration | BONUS (M4 yatırım skoru için) |
| Demografik veri | Next.js hydration | BONUS (M4 için) |
| Fiyat geçmişi | Next.js hydration | BONUS (price_history tablosu için) |
| Bölge fiyat trendi | Next.js hydration | BONUS (enflasyon kontrol için) |

**ÇOK ÖNEMLİ NOT:** Endeksa verisi Emlakjet'e Endeksa tarafından sağlanıyor. Bu veriyi saklarken atıf ("Kaynak: Endeksa") yapmak gerekir.

---

## 5. Sıradaki Adımlar (Hafta 2 Başlangıcı)

### 5.1 Önceliklendirilmiş To-Do

1. [ ] **Veri kaynağı analizi dokümanını tamamla** → `docs/veri_kaynagi_analizi.md`
   - Bu dosyadaki Emlakjet bulgularını aktar
   - Danışman toplantısında gösterilecek

2. [ ] **Scrapy spider'ı yaz** → `scraper/emlak_scraper/spiders/emlakjet_spider.py`
   - 3 katmanlı parsing (JSON-LD + dataLayer + hydration)
   - Rate limiting: 1-2 saniye/istek (robots.txt'de crawl-delay yok ama saygılı ol)
   - User-Agent: kurumsal kimlik (e.g. `EmlakPlatformuBot/1.0 (+https://github.com/fakbayrak/emlak-platformu)`)
   - Error handling + retry

3. [ ] **Pilot scraping (Hafta 2 ortası)**
   - Hedef: Balıkesir-Altıeylül, 100-500 ilan
   - Hem satılık hem kiralık
   - Veri kalitesi değerlendirmesi

4. [ ] **ETL pipeline** → `ml/src/data/etl.py`
   - Scrapy output → PostgreSQL listings tablosu
   - Duplicate detection (`id` üzerinden)
   - Veri doğrulama (Pydantic model)

5. [ ] **Pilot EDA**
   - Eksik değer analizi
   - Dağılım grafikleri
   - Aykırı değer tespiti
   - `ml/notebooks/01_eda_pilot.ipynb`

### 5.2 Danışman Toplantısı

- `01_proje_oneri_v2.docx` onayı bekleniyor
- Veri kaynağı seçimi (Emlakjet) onaya sunulmalı

---

## 6. Açık Konular / Kararlar

- [x] Sahibinden dışlandı (robots.txt yasak + teknik zorluk + hukuki risk)
- [x] Emlakjet seçildi (teknik ve etik açıdan ideal)
- [x] Playwright gereksiz, Scrapy yeterli
- [ ] Hepsiemlak'tan yedek veri alıp almayacağımız (Emlakjet yeterli gelirse gereksiz)
- [ ] Endeksa verisi atıfı için proje raporuna not eklenmeli

---

## 7. Teknik Detay Notları

### Docker Container'ları

```bash
docker-compose up -d
# PostgreSQL: localhost:5432 (db: emlak, user: postgres, password: .env'de)
# MLflow: localhost:5000
```

### Alembic Migration

```bash
cd backend
alembic upgrade head
# Mevcut revision: 84bc1dfaddce (initial schema)
```

### Test Komutları

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test
```

### CI/CD

- `.github/workflows/backend-ci.yml` — Ruff + Black + pytest
- `.github/workflows/frontend-ci.yml` — ESLint + Vitest + build
- `.github/workflows/model-ci.yml` — Ruff + model testleri (placeholder)

### Yapılan Düzeltmeler

- `backend/pyproject.toml` — Ruff kuralları (E/F/W/I, tests/alembic per-file ignore)
- `frontend/src/vite-env.d.ts` — TypeScript `import.meta.env` tip tanımı
- `frontend/package.json` — `"test": "vitest --passWithNoTests"`
- `frontend/src/App.test.tsx` — Placeholder test dosyası

---

## 8. Yeni Sohbete Başlangıç Mesajı (Şablon)

Yeni sohbet açınca bu mesajla başla (veya modifiye et):

> Merhaba Claude, bitirme projeme devam ediyoruz. Proje dokümanları `/mnt/project/` içinde. Özellikle `docs/sohbet_ozeti_hafta1_sonu.md` dosyasını oku — önceki sohbette aldığımız tüm kararlar orada.
>
> Özet: Hafta 1'i bitirdik, Emlakjet'i veri kaynağı olarak seçtik (3 katmanlı scraping stratejisi: JSON-LD + dataLayer + Next.js hydration). Şimdi Hafta 2'deyiz ve Scrapy spider yazmamız gerekiyor.
>
> Başlayalım mı?

---

**Bu doküman yazıldığı an itibarıyla son güncel durumu yansıtır.**
**Yeni kararlar alındıkça güncellenmelidir.**
