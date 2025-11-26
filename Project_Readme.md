## 🧮 Calculator Agent – Project README

### Genel Bakış

Calculator Agent, Google Gemini Gen AI SDK kullanarak çeşitli matematiksel domain’lerde hesaplama yapan, **modüler** ve **genişletilebilir** bir Python 3.11+ projesidir.  

Agent:
- Kullanıcı girdisini doğal dil veya komut formatında alır,
- Güvenlik ve validasyondan geçirir,
- İlgili hesaplama modülüne yönlendirir,
- Gemini’den gelen cevabı `CalculationResult` Pydantic modeliyle normalize eder,
- Sonucu metin + opsiyonel grafik olarak kullanıcıya sunar.

Bu README, projeyi bir ürün/proje olarak anlatır; hackathon oyunlaştırma detayları için ana `README.md` dosyasına bakabilirsiniz.

---

## Özellikler

### Desteklenen Domain’ler

- **Basic Math (`basic_math`)**
  - Dört işlem (+, −, \*, /)
  - Karekök, logaritma, trigonometrik fonksiyonlar vb.
  - Hızlı ve hafif çözümler, Gemini’ye minimum bağımlılık

- **Calculus (`calculus`)**
  - Limit, türev, integral, Taylor serileri, gradient
  - Örnek: `!calculus derivative x^3 at x=2`

- **Linear Algebra (`linear_algebra`)**
  - Matris çarpımı, determinant, özdeğer/özvektör, lineer sistem çözümü
  - Matris sonuçları Pydantic modelinde matris tipi (`List[List[float]]`) olarak tutulur

- **Financial (`financial`)**
  - NPV, IRR, bileşik faiz, kredi ödeme planı
  - **Decimal** tabanlı, float kullanılmıyor (hassas finansal hesaplar)

- **Equation Solver (`equation_solver`)**
  - Doğrusal ve polinom denklemler
  - Çoklu kök çıktıları (ör. `[x1, x2]`)

- **Graph Plotter (`graph_plotter`)**
  - 2D grafik üretimi (matplotlib + `Agg` backend)
  - Sonuçta PNG dosya yolu ve opsiyonel interaktif çıktı
  - Basit cache mantığı (`cache/` klasörü)

- **Statistics (`statistics`)**
  - Ortalama, medyan, mod
  - Standart sapma, varyans
  - Korelasyon, basit regresyon
  - Z-score, percentiles

---

## Mimari

### Dizin Yapısı (Özet)

```text
src/
  main.py                 # CLI & orchestrator
  config/
    settings.py           # Ayarlar + validate()
    prompts.py            # Her domain için Gemini prompt’ları
  core/
    agent.py              # GeminiAgent + RateLimiter
    parser.py             # Komut yönlendirme (!prefix / doğal dil)
    validator.py          # Input güvenliği ve sanitization
  modules/
    base_module.py        # Tüm modüller için ABC
    basic_math.py
    calculus.py
    linear_algebra.py
    financial.py
    equation_solver.py
    graph_plotter.py
    statistics.py
  schemas/
    models.py             # CalculationResult Pydantic modeli
  utils/
    exceptions.py         # Domain spesifik exception hiyerarşisi
    helpers.py            # Ortak yardımcı fonksiyonlar
    logger.py             # JSON tabanlı logging
tests/
  ...                     # config/core/modules/utils/integration testleri
```

### Ana Bileşenler

- **`GeminiAgent` (`src/core/agent.py`)**
  - Google Gemini istemcisi
  - `generate_json_response(prompt: str)` ile JSON döndüren yardımcı
  - Rate limiting (dakika başına çağrı) ve retry/backoff içerir

- **`RateLimiter`**
  - `calls_per_minute` parametresiyle yapılandırılır
  - Gemini için minimum 1 saniyelik bekleme garantisi sağlar

- **`CalculatorAgent` (`src/main.py`)**
  - Tüm modülleri bir araya getiren orchestrator
  - Kullanıcı girdisini `CommandParser` ile çözümler
  - `InputValidator` ile sanitization yapar
  - Doğru modüle yönlendirir ve formatlanmış sonuç döndürür

- **`BaseModule` (`src/modules/base_module.py`)**
  - Tüm modüller için abstract base class
  - Ortak alanlar: `gemini_agent`, `validator`, `domain_prompt`
  - Abstract metotlar:
    - `async def calculate(self, expression: str, **kwargs) -> CalculationResult`
    - `def _get_domain_prompt(self) -> str`

- **`CalculationResult` (`src/schemas/models.py`)**
  - Pydantic modeli:
    - `result`: `Union[float, List[float], Matrix, Dict[str, Any], str]`
    - `steps`: `List[str]`
    - `visual_data`: opsiyonel görselleştirme bilgisi
    - `confidence_score`: `float`
    - `domain`: `str` (zorunlu)

- **`InputValidator` (`src/core/validator.py`)**
  - `sanitize_expression` ile:
    - Boş / yanlış tipte girişleri reddeder
    - `__import__`, `eval(`, `exec(`, `os.`, `subprocess` gibi pattern’lerde `SecurityViolationError` fırlatır
  - `validate_numeric_expression` ile regex tabanlı karakter seti kontrolü yapar

- **`JSONFormatter` & `setup_logger` (`src/utils/logger.py`)**
  - Tüm logları JSON formatında üretir
  - Logger/handler level uyumlu, duplicate handler’lar temizlenmiş
  - Root logger’dan izole çalışır (`propagate=False`)

---

## Kurulum

### Gereksinimler

- Python **3.11+**
- Bir Gemini API anahtarı (`GEMINI_API_KEY`)

### Adımlar

```bash
git clone <repo-url>
cd ai-builder-challenge-hackathon

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# .env içine gerçek GEMINI_API_KEY değerini yazın
```

`src/config/settings.py` içindeki `Settings.validate()` çağrısı,  
placeholder (`"your_gemini_api_key"`) veya boş API key kullanımını engeller.

---

## Çalıştırma

### CLI – Tek Komut Modu

```bash
python -m src.main "2 + 2"
python -m src.main "!calculus derivative x^3 at x=2"
python -m src.main "!linalg [[1,2],[3,4]] * [[5],[6]]"
python -m src.main "!statistics mean [1,2,3,4,5]"
```

### CLI – İnteraktif Mod

```bash
python -m src.main
```

Örnek oturum:

```text
🧮 Calculator Agent - AI Builder Challenge
Version: 1.0.0

Kullanilabilir komutlar:
  - !calculus <ifade>   : Kalkulus islemleri
  - !linalg <ifade>     : Lineer cebir
  - !solve <ifade>      : Denklem cozme
  - !plot <ifade>       : Grafik cizme
  - !finance <ifade>    : Finansal hesaplamalar
  - !statistics <ifade> : Istatistik islemleri
  - <ifade>             : Temel matematik
```

---

## Konfigürasyon

### `src/config/settings.py`

- Önemli alanlar:
  - `GEMINI_API_KEY`: `.env` dosyasından okunur
  - `GEMINI_MODEL`: varsayılan `"gemini-2.5-flash"`
  - `RATE_LIMIT_CALLS_PER_MINUTE`

`Settings.validate()` tipik olarak uygulama başında çağrılır:

```python
from src.config.settings import settings

settings.validate()  # API key yoksa veya placeholder ise ValueError fırlatır
```

---

## Testler

### Çalıştırma

```bash
pytest -v
pytest --cov=src --cov-report=html
```

Önemli test dosyaları:

- `tests/core/test_agent.py`
- `tests/core/test_parser.py`
- `tests/core/test_validator.py`
- `tests/modules/test_*.py`
- `tests/test_integration.py`

### Mock Stratejisi

- `tests/conftest.py` içindeki `mock_gemini_agent` fixture’ı:
  - Varsayılan olarak nötr bir cevap döner
  - Her test kendi `return_value`’sunu override eder

Bu sayede:
- Farklı ifadeler için farklı sonuçlar test edilebilir,
- Domain alanı her zaman modül tarafından set edilir,
- Silent failure’lar (örneğin yanlış default 42.0) engellenir.

---

## Güvenlik Notları

- **InputValidator**:
  - `FORBIDDEN_PATTERNS` listesi ile zararlı pattern’leri engeller
  - İhlal durumunda `SecurityViolationError` fırlatır

- **Settings.validate**:
  - Boş veya placeholder API key kullanımını engeller
  - Gerekirse ortam değişkenlerini CI ortamında dummy fakat geçerli formatta tutun

- **Logging**:
  - JSON logging, hassas alanları maskelenecek şekilde yapılandırılabilir
  - Üretim ortamında logların merkezi bir sistemde toplanması önerilir

---

## Geliştirme Rehberi

### Yeni Modül Eklemek İçin

1. `src/modules/base_module.py`’den miras alan yeni bir sınıf oluşturun.
2. `src/config/prompts.py` içine domain’e özel prompt ekleyin.
3. Yeni domain için `CalculationResult` alanları yeterliyse doğrudan, değilse `metadata` altında ek bilgi sağlayın.
4. `src/core/parser.py` içerisinde yeni prefix/keyword desteği ekleyin.
5. `src/modules/__init__.py` ve `src/main.py`’de modülü export edip agent’a kaydedin.
6. `tests/modules/test_<modul>.py` ile en az %90 coverage hedefleyin.

### Kodlama Standartları

- Tüm Gemini çağrıları **async/await** ile yapılmalı.
- Tüm public fonksiyonlarda **type hints** bulunmalı.
- Docstring formatı: **Google style**.
- `print` yerine her zaman `logger` kullanılmalı.
- Hata mesajları kullanıcı dostu, mümkünse Türkçe olmalı.

---

## Özet

Calculator Agent, çok domain’li matematiksel hesaplamaları Gemini üzerinden yapan, modüler ve güçlü test altyapısına sahip bir ajandır. Güvenlik, logging ve test mimarisi; gerçek dünyada üretime alınabilir bir hesap makinesi agent’ı için referans alınacak şekilde tasarlanmıştır.  

Yeni domain’ler veya özellikler eklerken bu README’yi mimari ve stil rehberi olarak kullanabilirsiniz.


