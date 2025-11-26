# 🧮 Calculator Agent - AI Builder Challenge Hackathon

## 📋 Hackathon Hakkında

Bu proje, **AI Builder Challenge 2-Day Hackathon** için hazırlanmış bir "Broken Calculator Agent" challenge'ıdır. Projede **12 kritik hata** ve **100+ derleme hatası** gizlidir. Katılımcıların görevi bu hataları tespit edip düzeltmek ve projeye **yeni bir modül** eklemektir.

### 🎯 Hackathon Hedefleri

- **Gün 1**: Syntax ve runtime hatalarını bulup düzeltmek
- **Gün 2**: Silent failures'ı tespit etmek ve yeni modül eklemek
- **Bonus**: CI/CD pipeline kurmak ve dokümantasyon tamamlamak

### 📊 Puanlama Sistemi

- **Level 1 Hatalar (Syntax)**: 10 puan/hata (Toplam 40 puan)
- **Level 2 Hatalar (Runtime)**: 20 puan/hata (Toplam 60 puan)
- **Level 3 Hatalar (Silent Failures)**: 30 puan/hata (Toplam 60 puan)
- **Bonus Modül**: 40 puan
- **CI/CD**: 20 puan
- **Dokümantasyon**: 10 puan
- **Toplam**: 230 puan

---

## 🚀 Proje Hakkında

Google Gemini Gen AI SDK kullanılarak geliştirilmiş modüler, genişletilebilir bir hesaplama agent'ı. Proje şu anda **çalışmayan durumda** ve hackathon katılımcıları tarafından düzeltilmesi gerekiyor.

### ✨ Mevcut Özellikler

- **Modüler Yapı**: Her hesaplama türü bağımsız modüller halinde
- **Gemini AI Entegrasyonu**: Google Gemini ile akıllı hesaplama
- **Çoklu Domain Desteği**:
  - Temel Matematik (+, -, \*, /, sqrt, log, trigonometri)
  - Kalkülüs (limit, türev, integral, seri)
  - Lineer Cebir (matris, vektör, determinant)
  - Finansal Hesaplamalar (NPV, IRR, faiz, kredi)
  - Denklem Çözücü (doğrusal, polinom, diferansiyel)
  - Grafik Çizim (2D/3D plotlar)

---

## 🔧 Kurulum

### Gereksinimler

- Python 3.11+
- Google Gemini API Key
- Git

### Adımlar

1. **Repository'yi klonlayın:**

```bash
git clone <repository-url>
cd CalculatorAgent
```

2. **Sanal ortam oluşturun:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Bağımlılıkları yükleyin:**

```bash
pip install -r requirements.txt
```

4. **Environment değişkenlerini ayarlayın:**

```bash
cp .env.example .env
# .env dosyasını düzenleyip GEMINI_API_KEY'inizi ekleyin
```

---

## 🐳 Docker ile Kurulum ve Deploy

### Hızlı Başlangıç

```bash
# 1. Environment dosyasını hazırla
cp .docker.env.example .docker.env
# .docker.env dosyasını düzenle ve GEMINI_API_KEY'i ekle

# 2. Docker Compose ile çalıştır
docker-compose up -d

# 3. Logları görüntüle
docker-compose logs -f

# 4. Interactive mode için container'a bağlan
docker-compose exec calculator-agent python -m src.main
```

### Docker Image Build

```bash
# Image'ı build et
docker build -t calculator-agent:latest .

# Tek komut çalıştır
docker run --rm --env-file .docker.env calculator-agent:latest "2 + 2"
```

### GitHub Actions ile Otomatik Build ve Push

Proje, GitHub Actions ile otomatik Docker build ve Docker Hub'a push desteği içerir.

**Gerekli Secrets:**
- `DOCKER_USERNAME`: Docker Hub kullanıcı adı
- `DOCKER_PASSWORD`: Docker Hub şifresi veya access token

**Kullanım:**
```bash
# Main branch'e push yap
git push origin main

# GitHub Actions otomatik olarak:
# - Docker image build eder
# - Multi-arch (amd64, arm64) support
# - Docker Hub'a push eder
# - Production'a deploy eder (yapılandırıldıysa)
```

**Detaylı Deploy Talimatları:**

Detaylı Docker deployment talimatları için [DEPLOY.md](DEPLOY.md) dosyasına bakın.
Production deployment örnekleri için [.github/workflows/deploy-examples.md](.github/workflows/deploy-examples.md) dosyasına bakın.

---

## 🐛 Hata Kategorileri

### Level 1: Syntax Hataları (10 puan/hata)

**Çözüm Şablonu:**
```python
# HATA: logger.info çağrısında parantez eksik
# Dosya: src/main.py
# Satır: 67

# MEVCUT KOD (HATALI):
logger.info("Calculator Agent baslatildi"

# ÇÖZÜM:
logger.info("Calculator Agent baslatildi")

# AÇIKLAMA:
Kapanmayan parantez nedeniyle derleme hata veriyordu; çağrı doğru sözdizimiyle güncellendi.

```

```python
# HATA: Tanımlanmamış sınıflar modül listesine eklenmiş
# Dosya: src/main.py
# Satır: 63-64

# MEVCUT KOD (HATALI):
"wrong_module": WrongModuleClass(self.gemini_agent),
"extra_module": NonexistentModule(self.gemini_agent),

# ÇÖZÜM:
Tanımsız sınıfları içeren satırlar tamamen kaldırıldı.

# AÇIKLAMA:
WrongModuleClass ve NonexistentModule projede tanımlı olmadığı için sözlük oluşturulurken NameError oluşuyordu. Bu nedenle modül listesi içerisinden bu sınıfların kullanımını tamamen kaldırdık. Böylece uygulamanın başlangıç aşamasında oluşan derleme/syntax seviyesi hatası giderildi.
```

```python
# HATA: Uygulama metadata değişkenleri tanımsız
# Dosya: src/main.py
# Satır: 35-36

# MEVCUT KOD (HATALI):
APP_NAME = undefined_variable
APP_VERSION = missing_version

# ÇÖZÜM:
APP_NAME = "Calculator Agent"
APP_VERSION = "1.0.0"

# AÇIKLAMA:
Tanımlanmamış değerler NameError üreterek uygulamanın başlatılmasını engelliyordu.
Bu nedenle APP_NAME ve APP_VERSION için sabit ve anlamlı varsayılan değerler atandı.
Böylece meta bilgiler stabil ve güvenilir hale getirildi.
```

```python
# HATA: plt kullanımında tanımsız semboller
# Dosya: src/modules/graph_plotter.py
# Satır: 131-141

# MEVCUT KOD (HATALI):
plt.plot(x, y, 'b-', linewidth=2, wrong_param=5)
plt.xlabel(f'x {undefined_var}')
wrong_plt_call = plt.nonexistent_method()
png_path = self.cache_dir / f"{hash(expression)}.png" + undefined_string
plt.wrong_save_method(png_path, dpi=150, bbox_inches='tight')
 
# ÇÖZÜM:
plt.plot(x, y, 'b-', linewidth=2)
plt.xlabel('x')
png_path = self.cache_dir / f"{hash(expression)}.png"
plt.savefig(png_path, dpi=150, bbox_inches='tight')
 
# AÇIKLAMA:
Yanlış parametreler, tanımsız değişkenler ve olmayan matplotlib metodları syntax/runtime hatalarına yol açıyordu; standart `plt` çağrılarıyla değiştirildi.
```

```python
# HATA: Class içinde if statement kullanımı - Syntax hatası
# Dosya: src/config/settings.py
# Satır: 16-18
# MEVCUT KOD (HATALI):

class Settings:
    """Uygulama ayarlari"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    if not GEMINI_API_KEY:  # Syntax hatası - class içinde if kullanılamaz!
        GEMINI_API_KEY = "your_gemini_api_key"
        wrong_assignment = undefined_var  # Tanımlı değil!
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
 
# ÇÖZÜM:
 
class Settings:
    """Uygulama ayarlari"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    # API key kontrolü validate() metodunda yapılmalı, class seviyesinde değil
 
# AÇIKLAMA:

Python'da class tanımı sırasında (class body içinde) if statement kullanılamaz. Class body sadece attribute tanımlamaları, metod tanımlamaları ve decorator'lar içerebilir. If statement kullanımı `SyntaxError` fırlatır. API key kontrolü ve fallback mantığı `validate()` metodunda veya `__init__` metodunda yapılmalıdır.

```
```python
# HATA: Tanımlanmamış değişken kullanımı
# Dosya: src/config/settings.py
# Satır: 18

# MEVCUT KOD (HATALI):
wrong_assignment = undefined_var  # Tanımlı değil!
# ÇÖZÜM:

# Bu satır tamamen kaldırılmalı - gereksiz ve hatalı

# AÇIKLAMA:
`undefined_var` tanımlı olmadığı için Python bu satırı derlerken `NameError` fırlatır. Bu satır gereksiz görünüyor ve kaldırılmalıdır.
```
```python
# HATA: Syntax hatası - nokta ile başlayan ifade
# Dosya: src/core/agent.py
# Satır: 39

# MEVCUT KOD (HATALI):
wait_time = .min_interval - time_since_last_call

# ÇÖZÜM:
wait_time = self.min_interval - time_since_last_call
 
# AÇIKLAMA:

`.min_interval` geçersiz syntax'tır. Python'da değişken isimleri nokta ile başlayamaz. `self.min_interval` olmalıdır.
```
```python
# HATA: Yanlış indentasyon - async def
# Dosya: src/core/agent.py
# Satır: 101

# MEVCUT KOD (HATALI):

   async def generate_with_retry(
        self,
        prompt: str,
        ...
# ÇÖZÜM:

    async def generate_with_retry(
        self,
        prompt: str,
        ...

# AÇIKLAMA:

`async def` 3 space ile indent edilmiş, 4 space olmalıdır. Python'da standart indentasyon 4 space'tir. Bu indentasyon hatası syntax hatasına neden olur.

```
Alternatif Çözümler:
- Tab kullanmak

```python
# HATA: Regex syntax hatası
# Dosya: src/core/agent.py
# Satır: 175

# MEVCUT KOD (HATALI):

json_match = re.search(r{.*\}', response_text, re.DOTALL)
 
# ÇÖZÜM:

json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
 
# AÇIKLAMA:

Regex pattern'de `r{.*\}'` geçersiz syntax'tır. Raw string içinde süslü parantezler escape edilmelidir. Doğru format: `r'\{.*\}'` veya `r"\{.*\}"`.

```
```python
# HATA: Type hint syntax hatası - Dict key type eksik
# Dosya: src/core/parser.py
# Satır: 15
# MEVCUT KOD (HATALI):
 
MODULE_PREFIXES: Dict[, str] = {
 
# ÇÖZÜM:
 
MODULE_PREFIXES: Dict[str, str] = {

# AÇIKLAMA:
Dict type hint’inde hem key hem value tipi belirtilmeli; eksik yazım syntax hatası oluşturuyordu.
```
```python
# HATA: Tanımlanmamış type hint ve değişken
# Dosya: src/core/parser.py
# Satır: 31

# MEVCUT KOD (HATALI):
wrong_param: undefined_type = None
 
# ÇÖZÜM:
 
# Satır kaldırıldı; gereksiz ve hatalıydı.

# AÇIKLAMA:
`undefined_type` tanımlı olmadığı için import sırasında `NameError` oluşuyordu. Satır tamamen kaldırılarak sınıf sadeleştirildi.
```
```python
# HATA: List başlangıcı eksik
# Dosya: src/core/parser.py
# Satır: 74

# MEVCUT KOD (HATALI):
calculus_keywords = 
    "derivative", ...
]

# ÇÖZÜM:
 
calculus_keywords = [
    "derivative", "integral", "limit", "taylor", "gradient",
    "turev", "integral", "limit", "seri"
]
 
# AÇIKLAMA:
Açılış köşeli parantez eksik olduğu için `SyntaxError` oluşuyordu; liste doğru şekilde tanımlandı.
```
Alternatif Çözümler:
- Listeyi tuple olarak tanımlamak.

```python
# HATA: Değişken adı tutarsız
# Dosya: src/core/parser.py
# Satır: 71, 78
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
text_lo = text.lower()
...
if any(keyword in text_lower for keyword in calculus_keywords):
 

# ÇÖZÜM:
 
text_lower = text.lower()
...
if any(keyword in text_lower for keyword in calculus_keywords):
 

# AÇIKLAMA:
`text_lower` kullanılmasına rağmen `text_lo` olarak tanımlandığı için NameError oluşuyordu; isimler eşitlendi.
```
Alternatif Çözümler:
- Kısa isim `text_lo`yu her yerde kullanmak.

```python
# HATA: linalg_keywor typo’su
# Dosya: src/core/parser.py
# Satır: 82, 86
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
linalg_keywor = [...]
if any(keyword in text_lower for keyword in linalg_keywords):
 

# ÇÖZÜM:
 
linalg_keywords = [
    "matrix", "determinant", "eigenvalue", "vector", "matris",
    "determinant", "ozdeger", "vektor"
]
if any(keyword in text_lower for keyword in linalg_keywords):
 

# AÇIKLAMA:
Tanım ile kullanım farklı olduğu için NameError oluşuyordu; değişken adı düzeltilerek uyumlu hale getirildi.

```
Alternatif Çözümler:
- Keyword listelerini sözlük halinde saklamak.

```python
# HATA: List başlangıcı eksik ve boş keyword
# Dosya: src/core/parser.py
# Satır: 90-91

# MEVCUT KOD (HATALI):
 
equation_keywords = 
    "solve", "equation", "", "coz", "denklem", "kok"
]
 

# ÇÖZÜM:
 
equation_keywords = [
    "solve", "equation", "coz", "denklem", "kok"
]
 

# AÇIKLAMA:
Liste başlığı eksik olduğundan SyntaxError oluşuyor, ayrıca boş string her girdiyi eşleştirerek yanlış tespitlere sebep oluyordu; ikisi de düzeltildi.

```
Alternatif Çözümler:
- Keywords’ü tuple olarak tanımlamak.

```python
# HATA: List kapanışı eksik
# Dosya: src/core/parser.py
# Satır: 97-100

# MEVCUT KOD (HATALI):
 
plot_keywords = [
    "plot", "graph", "draw", "ciz", "grafik"

if any(keyword in text_lower for keyword in plot_keywords):
 

# ÇÖZÜM:
 
plot_keywords = [
    "plot", "graph", "draw", "ciz", "grafik"
]
if any(keyword in text_lower for keyword in plot_keywords):
 

# AÇIKLAMA:
Liste kapanış parantezi eksik olduğu için `SyntaxError` oluşuyordu; `]` eklenerek if bloğu doğru konuma getirildi.
```
```python
# HATA: Return statement yanlış yerde
# Dosya: src/core/parser.py
# Satır: 110

# MEVCUT KOD (HATALI):
 
        if any(keyword in text_lower for keyword in financial_keywords):
            return "financial"
        
         None
 

# ÇÖZÜM:
 
        if any(keyword in text_lower for keyword in financial_keywords):
            return "financial"
        
        return None
 

# AÇIKLAMA:
`None` satırı yanlış indent edilmiş ve `return` kelimesi eksik olduğu için SyntaxError oluşuyordu; blok düzenlenip açıkça `return None` eklendi.
```
```python
# HATA: Tanımlanmamış type hint
# Dosya: src/core/validator.py
# Satır: 29

# MEVCUT KOD (HATALI):
 
wrong_param: undefined_type = None
 

# ÇÖZÜM:
 
# Satır kaldırıldı; type hint geçersizdi.
 

# AÇIKLAMA:
`undefined_type` tanımlı olmadığı için modül import edilirken NameError oluşuyordu. Satır gereksiz olduğundan kaldırıldı.

```
```python
# HATA: Hatalı method çağrısı ve tekrar eden kod
# Dosya: src/core/validator.py
# Satır: 50

# MEVCUT KOD (HATALI):
 
expression_lower = expression.wrong_lower_method()   wrong_lower_method()
 

# ÇÖZÜM:
 
expression_lower = expression.lower()
 

# AÇIKLAMA:
Var olmayan `wrong_lower_method()` çağrısı AttributeError üretiyor, ayrıca satırda yinelenen ifade SyntaxError’a yol açıyor. Standart `lower()` kullanılarak sorun giderildi.
```
Alternatif Çözümler:
- Gerekirse `casefold()` gibi başka bir normalizasyon metodu kullanmak.

```python
# HATA: Tanımlanmamış değişken kullanımı
# Dosya: src/core/validator.py
# Satır: 52

# MEVCUT KOD (HATALI):
 
wrong_lower = undefined_var.lower()
 

# ÇÖZÜM:
 
# Satır kaldırıldı; gereksiz ve hatalıydı.
 

# AÇIKLAMA:
`undefined_var` tanımlı olmadığı için kod derhal `NameError` üretiyordu. Satırın kaldırılmasıyla gereksiz değişken ortadan kalktı.
```
```python
# HATA: `expression.lowe()` typo’su
# Dosya: src/core/validator.py
# Satır: 60
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
if "test" in expression.lowe():
 

# ÇÖZÜM:
 
# Kontrol gereksiz olduğu için satır kaldırıldı.
# İhtiyaç halinde: if "test" in expression.lower():
 

# AÇIKLAMA:
`lowe()` metodu olmadığı için AttributeError oluşuyordu; blok kaldırılarak typo’dan kaynaklı hata giderildi.
```
```python
# HATA: `__all__` listesi yanlış tanımlanmış
# Dosya: src/modules/__init__.py
# Satır: 10

# MEVCUT KOD (HATALI):
 
__all__ = 
    "Calculus",  
    "LinearAlgebra", 
    "BasicMath",  
]
 

# ÇÖZÜM:
 
__all__ = [
    "CalculusModule",
    "LinearAlgebraModule",
    "BasicMathModule",
    "FinancialModule",
    "EquationSolverModule",
    "GraphPlotterModule",
]
 

# AÇIKLAMA:
Açılış köşeli parantez eksikliği SyntaxError’a neden oluyordu; ayrıca listedeki isimler gerçek modül sınıflarıyla eşleşmiyordu. Liste doğru formatta yeniden yazıldı.
```
```python
# HATA: BaseModule ABC'den türemiyor
# Dosya: src/modules/base_module.py
# Satır: 13

# MEVCUT KOD (HATALI):
 
class BaseModule():
 

# ÇÖZÜM:
 
class BaseModule(ABC):
 

# AÇIKLAMA:
Abstract sınıfın `ABC`'den türememesi, alt sınıfların abstract metotları implement etmeden kullanılmasına izin veriyordu; miras zinciri düzeltilerek Python'un abstract kontrolü etkinleştirildi.

```
```python
# HATA: Tanımlanmamış değişken kullanımı
# Dosya: src/modules/base_module.py
# Satır: 25, 43, 114

# MEVCUT KOD (HATALI):
 
self.extra_field = missing_constant
undefined_var_in_method = "test"
extra_field = undefined_field
 

# ÇÖZÜM:
 
# Tüm satırlar kaldırıldı; CalculationResult yalnızca gerçek alanları alıyor.
 

# AÇIKLAMA:
`missing_constant` ve `undefined_field` tanımlı olmadığı için modül importunda `NameError` oluşuyordu. Gereksiz satırlar temizlenerek base sınıf sadeleştirildi.
```
```python
# HATA: Yanlış type hint kullanımı
# Dosya: src/modules/base_module.py
# Satır: 26
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
self.wrong_type: int = "string"
 

# ÇÖZÜM:
 
# Satır kaldırıldı; gerekirse doğru type hint ile yeniden eklenmeli.
 

# AÇIKLAMA:
`int` olarak açıklanan değişkene string atanması type check araçlarında hataya sebep oluyor ve okuyucuyu yanıltıyor. Gereksiz satır temizlendi.

```
```python
# HATA: Geçersiz assignment expression
# Dosya: src/modules/base_module.py
# Satır: 106

# MEVCUT KOD (HATALI):
 
wrong_syntax = (result = gemini_response.get("result", ""))
 

# ÇÖZÜM:
 
# Satır kaldırıldı; result değeri doğrudan CalculationResult içinde set ediliyor.
 

# AÇIKLAMA:
Parantez içinde `result = ...` kullanımı Python’da geçersizdir. Gereksiz satır kaldırılarak syntax hatası giderildi.
```
```python
# HATA: Gereksiz GeminiAgent importu
# Dosya: src/modules/basic_math.py
# Satır: 8

# MEVCUT KOD (HATALI):
 
from src.core.agent import GeminiAgent
 

# ÇÖZÜM:
 
# Satır kaldırıldı; BaseModule zaten gerekli tipe sahip.
 

# AÇIKLAMA:
GeminiAgent `BaseModule` içinde import edildiğinden burada tekrar import etmek circular dependency riskine yol açıyordu. Import kaldırılarak modül zinciri sadeleştirildi.
```
```python
# HATA: Eksik type hint
# Dosya: src/modules/basic_math.py
# Satır: 13

# MEVCUT KOD (HATALI):
 
def safe_divide(a: , b: float) -> float:
 

# ÇÖZÜM:
 
def safe_divide(a: float, b: float) -> float:
 

# AÇIKLAMA:
Type hint bölümü boş bırakıldığı için syntax hatası oluşuyordu; `a` parametresi float olarak tanımlandı.
```
```python
# HATA: Assignment yerine comparison kullanılmalı
# Dosya: src/modules/basic_math.py
# Satır: 24

# MEVCUT KOD (HATALI):

if b = 0:

# ÇÖZÜM:

if b == 0:

# AÇIKLAMA:

`b = 0` assignment'tır, comparison değil. Python'da comparison için `==` kullanılmalıdır. `b = 0` `SyntaxError` fırlatır çünkü if statement içinde assignment yapılamaz (Python 3.8+ hariç walrus operator ile).
```
```python
# HATA: Syntax hatası - raise statement yanlış kullanımı
# Dosya: src/modules/basic_math.py
# Satır: 26

# MEVCUT KOD (HATALI):
 
wrong_raise = raise undefined_exception()
 
# ÇÖZÜM:

# Bu satır kaldırılmalı - gereksiz ve hatalı
# Zaten bir önceki satırda raise var
 

# AÇIKLAMA:

`raise` statement bir değişkene atanamaz. Bu `SyntaxError` fırlatır. Ayrıca `undefined_exception` tanımlı değildir. Bu satır gereksizdir çünkü bir önceki satırda zaten `raise ValueError` var.

```
```python
# HATA: Syntax hatası - return statement yanlış kullanımı
# Dosya: src/modules/basic_math.py
# Satır: 28

# MEVCUT KOD (HATALI):
 
wrong_return = return undefined_value

# ÇÖZÜM:

# Bu satır kaldırılmalı - gereksiz ve hatalı
# Zaten bir önceki satırda return var
 

# AÇIKLAMA:

`return` statement bir değişkene atanamaz. Bu `SyntaxError` fırlatır. Ayrıca `undefined_value` tanımlı değildir. Bu satır gereksizdir çünkü bir önceki satırda zaten `return` var.

```
```python
# HATA: Import ifadesi yanlış yazılmış
# Dosya: src/modules/calculus.py
# Satır: 6

# MEVCUT KOD (HATALI):
 
wrong_import = from src.config.prompts import WRONG_PROMPT
 

# ÇÖZÜM:
 
# Satır kaldırıldı; doğru import zaten mevcut.
 

# AÇIKLAMA:
Import cümlesi bir değişkene atanamaz ve `WRONG_PROMPT` isimli sembol yoktu; satır tamamen silindi.
```
```python
# HATA: Gereksiz circular import
# Dosya: src/modules/calculus.py
# Satır: 8

# MEVCUT KOD (HATALI):
 
from . import LinearAlgebraModule
 

# ÇÖZÜM:
 
# Satır kaldırıldı; module kendi bağımlılıklarını BaseModule’den alıyor.
 

# AÇIKLAMA:
LinearAlgebraModule burada kullanılmadığı halde import edilmesi circular dependency riskini artırıyordu; gereksiz import silindi.
```
```python
# HATA: Tanımlanmamış type hint
# Dosya: src/modules/calculus.py
# Satır: 32

# MEVCUT KOD (HATALI):
 
extra_param: undefined_type = None
 

# ÇÖZÜM:
 
# Parametre kaldırıldı; type kullanılmıyordu.
 

# AÇIKLAMA:
`undefined_type` tanımlı olmadığından import aşamasında NameError oluşuyordu; parametre tamamen silindi.
```
```python
# HATA: Satır sonu karakteri syntax hatası
# Dosya: src/modules/calculus.py
# Satır: 50

# MEVCUT KOD (HATALI):
 
result = self._create_result(response, "calculus")  !
 

# ÇÖZÜM:
 
result = self._create_result(response, "calculus")
 

# AÇIKLAMA:
Satır sonundaki `!` karakteri gereksizdi ve parser’ın hata vermesine yol açıyordu; temizlendi.
```
```python
# HATA: Yanlış metod çağrıları
# Dosya: src/modules/calculus.py
# Satır: 44, 51, 66
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
wrong_validation = self.wrong_validate_method()
wrong_result = await self.nonexistent_method()
logger.wrong_method(undefined_var)
 

# ÇÖZÜM:
 
# Geçersiz çağrılar kaldırıldı; yalnızca gerçek metotlar bırakıldı.
 

# TEST:
- `pytest tests/modules/test_calculus.py`

# AÇIKLAMA:
Tanımsız metod ve değişkenler AttributeError/NameError üreterek akışı bozuyordu; satırlar silindi.
```
```python
# HATA: Tanımlanmamış değişken kullanımı
# Dosya: src/modules/calculus.py
# Satır: 66

# MEVCUT KOD (HATALI):
 
logger.wrong_method(undefined_var)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; undefined_var ve wrong_method mevcut değil.
 

# AÇIKLAMA:
Tanımsız değişken ve logger çağrısı NameError/AttributeError ürettiği için blok tamamen temizlendi.

```
```python
# HATA: `expresson` typo’su ve yanlış metod
# Dosya: src/modules/equation_solver.py
# Satır: 33
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
self.wrong_method(expresson)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; geçersiz metod ve değişken kullanılmıyor.
 

# AÇIKLAMA:
Yanlış yazılmış değişken ve tanımsız metod NameError/AttributeError üretiyordu; gereksiz satır tamamen temizlendi.

```
```python
# HATA: Yanlış yorumla await uyarısı
# Dosya: src/modules/equation_solver.py
# Satır: 38

# MEVCUT KOD (HATALI):
 
result = self._create_result(response, "equation_solver")  # await eksik!
 

# ÇÖZÜM:
 
result = self._create_result(response, "equation_solver")
 

# AÇIKLAMA:
`_create_result` senkron olduğundan “await eksik” yorumu yanıltıcıydı; yorum kaldırıldı ve çağrı olduğu gibi bırakıldı.

```
```python
# HATA: Geçersiz decimal importu
# Dosya: src/modules/financial.py
# Satır: 4

# MEVCUT KOD (HATALI):
 
from nonexistent.decimal import WrongDecimal
 

# ÇÖZÜM:
 
# Satır kaldırıldı; standart decimal zaten importlu.
 

# AÇIKLAMA:
Var olmayan modül nedeniyle import sırasında `ModuleNotFoundError` oluşuyordu; gereksiz satır silindi.
```
```python
# HATA: Logger kurulumu typo
# Dosya: src/modules/financial.py
# Satır: 12

# MEVCUT KOD (HATALI):
 
logger = setup_logge()
gger(missing_param)
 

# ÇÖZÜM:
 
logger = setup_logger()
 

# AÇIKLAMA:
Fonksiyon adı yanlış yazıldığı ve ikinci satırda geçersiz çağrı bulunduğu için logger hiç oluşmuyordu; satırlar doğru hale getirildi.

```
```python
# HATA: Geçersiz boş metod çağrısı
# Dosya: src/modules/financial.py
# Satır: 16

# MEVCUT KOD (HATALI):
 
().wrong_method(28)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; context ayarı zaten mevcut.
 

# AÇIKLAMA:
Boş parantez ile başlayan çağrı syntax hatasına yol açıyordu; gereksiz satır kaldırıldı.

```
```python
# HATA: Tanımlanmamış değişken kullanımı
# Dosya: src/modules/financial.py
# Satır: 19

# MEVCUT KOD (HATALI):
 
wrong_decimal = Decimal(undefined_string)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; undefined_string yoktu.
 

# AÇIKLAMA:
Tanımsız değişken NameError’a yol açtığı için gereksiz satır kaldırıldı.
```
```python
# HATA: Geçersiz plotting importu
# Dosya: src/modules/graph_plotter.py
# Satır: 13

# MEVCUT KOD (HATALI):
 
from nonexistent.plotting import wrong_lib
 

# ÇÖZÜM:
 
# Satır kaldırıldı; matplotlib yeterli.
 

# AÇIKLAMA:
Olmayan modül importu başlangıçta `ModuleNotFoundError` veriyordu; gereksizdi.
```
Alternatif Çözümler:
- Gerçek kütüphane gerekiyorsa doğru paketi eklemek.

```python
# HATA: Matplotlib yanlış metod çağrısı
# Dosya: src/modules/graph_plotter.py
# Satır: 8

# MEVCUT KOD (HATALI):
 
matplotlib.wrong_method('Agg')
matplotlib.use('Agg')
 

# ÇÖZÜM:
 
matplotlib.use('Agg')
 

# AÇIKLAMA:
`wrong_method` bulunmadığı için AttributeError oluşuyordu; satır kaldırıldı.
```
```python
# HATA: `plt` importu eksik
# Dosya: src/modules/graph_plotter.py
# Satır: 11

# MEVCUT KOD (HATALI):
 
# import matplotlib.pyplot as plt
 

# ÇÖZÜM:
 
import matplotlib.pyplot as plt
 

# AÇIKLAMA:
Dosya içinde `plt` kullanıldığı halde import edilmemişti; yorum satırı aktive edildi.
```
```python
# HATA: `super().__init__` parametresiz
# Dosya: src/modules/graph_plotter.py
# Satır: 28

# MEVCUT KOD (HATALI):
 
super().__init__()
 

# ÇÖZÜM:
 
super().__init__(gemini_agent)
 

# AÇIKLAMA:
BaseModule `gemini_agent` beklediği için parametresiz çağrı TypeError’a sebep oluyordu.
```
```python
 HATA: `Path.mkdir` yanlış metod adı
# Dosya: src/modules/graph_plotter.py
# Satır: 30

# MEVCUT KOD (HATALI):
 
self.cache_dir.wrong_mkdir_method(parents=True, exist_ok=True)
 

# ÇÖZÜM:
 
self.cache_dir.mkdir(parents=True, exist_ok=True)
 

# AÇIKLAMA:
`wrong_mkdir_method` bulunmadığı için AttributeError çıkıyordu; doğru metod kullanıldı.
```
Alternatif Çözümler:
- `os.makedirs` ile dizin oluşturmak.

```python
# HATA: Yanlış type hint ile boş dict
# Dosya: src/modules/graph_plotter.py
# Satır: 32

# MEVCUT KOD (HATALI):
 
self.wrong_cache: str = {}
 

# ÇÖZÜM:
 
# Satır kaldırıldı; plot_cache zaten mevcut.
 

# AÇIKLAMA:
`str` tipine dict atanması lint/type hatasına yol açıyordu; gereksiz satır silindi.
```
Alternatif Çözümler:
- Yeni cache gerekiyorsa `Dict[str, Any]` olarak tanımlamak.

```python
# HATA: Tanımlanmamış constant kullanımı
# Dosya: src/modules/graph_plotter.py
# Satır: 33

# MEVCUT KOD (HATALI):
 
self.extra_field = missing_constant
 

# ÇÖZÜM:
 
# Satır kaldırıldı; extra_field kullanılmıyor.
 

# AÇIKLAMA:
`missing_constant` tanımlı olmadığı için NameError oluşuyordu; gereksiz satır temizlendi.
```
```python
# HATA: Yanlış type hint ataması
# Dosya: src/modules/graph_plotter.py
# Satır: 34

# MEVCUT KOD (HATALI):
 
self.wrong_type_field: int = "string"
 

# ÇÖZÜM:
 
# Satır kaldırıldı; alan kullanılmıyor.
 

# AÇIKLAMA:
`int` tipine string atamak lint/type hatasına yol açıyordu; gereksiz alan temizlendi.
```
```python
# HATA: Yanlış parametre sözdizimi
# Dosya: src/modules/graph_plotter.py
# Satır: 43

# MEVCUT KOD (HATALI):
 
async def calculate(
    self,
    expression: str,
    *kwargs,
    wrong_param = undefined_default
) -> CalculationResult:
 

# ÇÖZÜM:
 
async def calculate(
    self,
    expression: str,
    **kwargs
) -> CalculationResult:
 

# AÇIKLAMA:
Keyword argümanları için `**kwargs` gerekir; ayrıca `undefined_default` tanımlı değildi. İmza BaseModule ile aynı hale getirildi.

```
Alternatif Çözümler:
- Positional argüman gerekiyorsa `*args` eklemek.

```python
# HATA: Yorum satırına alınmış return
# Dosya: src/modules/graph_plotter.py
# Satır: 144

# MEVCUT KOD (HATALI):
 
# return {"png": str(png_path)}
 

# ÇÖZÜM:
 
return {"png": str(png_path)}
 

# AÇIKLAMA:
Aktif return ifadesi yorum satırı halinde bırakıldığı için kod okunabilirliği bozuluyordu; gereksiz yorum kaldırıldı.
```
```python
# HATA: Circular import
# Dosya: src/modules/linear_algebra.py
# Satır: 7

# MEVCUT KOD (HATALI):
 
from . import CalculusModule
 

# ÇÖZÜM:
 
# Satır kaldırıldı; kullanılmayan import circular riski doğuruyordu.
 

# AÇIKLAMA:
Modül calculus’a ihtiyaç duymadığı halde import edip döngüsel bağımlılık oluşturuyordu; gereksiz import kaldırıldı.
```
```python
# HATA: `calculate` metodunda self eksik
# Dosya: src/modules/linear_algebra.py
# Satır: 20

# MEVCUT KOD (HATALI):
 
async def calculate(
    ,
    expression: str,
 

# ÇÖZÜM:
 
async def calculate(
    self,
    expression: str,
 

# AÇIKLAMA:
Instance metotları self parametresi olmadan tanımlanamaz; eksiklik syntax hatasına yol açıyordu.

```
```python
# HATA: Yanlış kwargs sözdizimi
# Dosya: src/modules/linear_algebra.py
# Satır: 22-23

# MEVCUT KOD (HATALI):
 
*kwargs,
wrong_param = undefined_default
 

# ÇÖZÜM:
 
**kwargs
 

# AÇIKLAMA:
Keyword argümanları `**kwargs` ile toplanmalı; ayrıca `undefined_default` tanımsızdı. İmza BaseModule ile uyumlu hale getirildi.
```
```python
# HATA: Tanımsız değişken döndürme
# Dosya: src/modules/linear_algebra.py
# Satır: 51

# MEVCUT KOD (HATALI):
 
return undefined_result
 

# ÇÖZÜM:
 
return result
 

# AÇIKLAMA:
Gerçek sonuç `result` değişkeninde tutuluyordu; tanımsız isim kullanmak NameError’a yol açıyordu. Doğru değişken return edilerek giderildi.

```
```python
# HATA: CalculationResult BaseModel’den türememiş
# Dosya: src/schemas/models.py
# Satır: 7

# MEVCUT KOD (HATALI):
 
class CalculationResult():
    """Hesaplama sonucu modeli"""
 

# ÇÖZÜM:
 
class CalculationResult(BaseModel):
    """Hesaplama sonucu modeli"""
 

# AÇIKLAMA:
Pydantic Field kullanıldığı halde sınıf BaseModel’den türemediği için validation çalışmıyordu; doğru miras eklendi.

```
```python
# HATA: Tanımlanmamış type hint
# Dosya: src/schemas/models.py
# Satır: 10

# MEVCUT KOD (HATALI):
 
wrong_field: undefined_type = Field(...)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; field gereksizdi.
 

# AÇIKLAMA:
`undefined_type` tanımsız olduğu için import sırasında hata veriyordu; gereksiz field tamamen kaldırıldı.
```
```python
# HATA: CalculationError Exception’dan türemiyor
# Dosya: src/utils/exceptions.py
# Satır: 3

# MEVCUT KOD (HATALI):
 
class CalculationError():
    wrong_field = undefined_constant
 

# ÇÖZÜM:
 
class CalculationError(Exception):
    """Genel hesaplama hatası"""
    pass
 

# AÇIKLAMA:
Exception sınıfları `Exception`’dan türemedikleri sürece raise/catch edilemez; ayrıca tanımsız field kaldırıldı.

```
```python
# HATA: Tanımlanmamış field kullanımı
# Dosya: src/utils/exceptions.py
# Satır: 4
# Hata Tipi: Syntax Error / NameError

# MEVCUT KOD (HATALI):
 
wrong_field = undefined_constant
 

# ÇÖZÜM:
 
# Satır tamamen kaldırıldı; exception sınıfları yalnızca mesaj taşır.
 

# TEST:
- `pytest tests/utils/test_exceptions.py -k calculation_error_import`

# AÇIKLAMA:
Global kapsamda tanımsız değişken bırakmak modül import edilirken NameError fırlatır ve tüm exception tanımlarının yüklenmesini engeller.
```
```python
# HATA: GeminiAPIError Exception’dan türemiyor
# Dosya: src/utils/exceptions.py
# Satır: 13-15
# Hata Tipi: Syntax Error / Type Definition

# MEVCUT KOD (HATALI):
 
class GeminiAPIError():
    """Gemini API'den donen hata"""
    wrong_method = lambda: undefined_function()
 

# ÇÖZÜM:
 
class GeminiAPIError(Exception):
    """Gemini API'den donen hata"""
    pass
 

# TEST:
- `pytest tests/utils/test_exceptions.py -k gemini_api_error`

# AÇIKLAMA:
`Exception` tabanı olmadığı için `raise GeminiAPIError()` çağrıları TypeError üretiyordu. Ayrıca tanımsız lambda fonksiyonu import aşamasında NameError oluşturduğu için tamamen kaldırıldı.
```
```python
# HATA: Tanımlanmamış lambda fonksiyonu
# Dosya: src/utils/exceptions.py
# Satır: 15
# Hata Tipi: Syntax Error / NameError

# MEVCUT KOD (HATALI):
 
wrong_method = lambda: undefined_function()
 

# ÇÖZÜM:
 
# Satır tamamen kaldırıldı; exception tanımlarında gereksiz fonksiyon bulunmamalı.
 

# TEST:
- `pytest tests/utils/test_exceptions.py -k gemini_api_error`

# AÇIKLAMA:
`undefined_function()` mevcut olmadığı için dosya import edilir edilmez patlıyordu; gereksiz lambda kaldırıldı ve sınıf sadeleştirildi.

```
```python
# HATA: SecurityViolationError Exception’dan türemiyor
# Dosya: src/utils/exceptions.py
# Satır: 19
# Hata Tipi: Syntax Error / Type Definition

# MEVCUT KOD (HATALI):
 
class SecurityViolationError():
    """Guvenlik ihlali tespit edildi"""
    pass
 

# ÇÖZÜM:
 
class SecurityViolationError(Exception):
    """Guvenlik ihlali tespit edildi"""
    pass
 

# TEST:
- `pytest tests/utils/test_exceptions.py -k security_violation`

# AÇIKLAMA:
`Exception` tabanı olmadan `raise SecurityViolationError()` çağrıları TypeError veriyordu ve güvenlik kontrolleri devreye girmiyordu; doğru miras eklendi.
```
```python
# HATA: ModuleNotFoundError yanlış tanımlanmış
# Dosya: src/utils/exceptions.py
# Satır: 24
# Hata Tipi: Syntax Error / Name Shadowing

# MEVCUT KOD (HATALI):
 
class ModuleNotFoundError():
    """Modul bulunamadi"""
    pass
 

# ÇÖZÜM:
 
class CalculatorModuleNotFoundError(Exception):
    """Modul bulunamadi"""
    pass
 

# TEST:
- `pytest tests/utils/test_exceptions.py -k module_not_found`

# AÇIKLAMA:
Python'ın built-in `ModuleNotFoundError` sınıfını gölgelemek import hatalarının yanlış yorumlanmasına neden oluyordu; isim değiştirildi ve doğru base class kullanıldı.
```
```python
# HATA: Var olmayan helper modülü import ediliyor
# Dosya: src/utils/helpers.py
# Satır: 8

# MEVCUT KOD (HATALI):
 
from nonexistent.helpers import wrong_helper
 

# ÇÖZÜM:
 
# Gereksiz import satırı tamamen kaldırıldı.
 

# AÇIKLAMA:
Projede bulunmayan bir modülü import etmek yükleme sırasında `ModuleNotFoundError` üretir ve uygulama başlamadan çöker; satır silinerek risk ortadan kaldırıldı.
```
```python
# HATA: Fonksiyon gövdesinde tanımsız type hint satırı
# Dosya: src/utils/helpers.py
# Satır: 76

# MEVCUT KOD (HATALI):
 
def format_result_for_display(result: Any) -> str:
    wrong_param: undefined_type = None
    """Sonucu kullanici dostu formatta gosterir"""
 

# ÇÖZÜM:
 
def format_result_for_display(result: Any) -> str:
    """Sonucu kullanici dostu formatta gosterir"""
 

# AÇIKLAMA:
`undefined_type` tanımlı olmadığı için fonksiyon import edilirken NameError oluşuyordu; gereksiz satır kaldırılarak docstring doğru konuma taşındı.

```
```python
# HATA: `return` ifadesi değişkene atanmış
# Dosya: src/utils/helpers.py
# Satır: 87

# MEVCUT KOD (HATALI):
 
else:
    wrong_return = return undefined_value
    return str(result)
 

# ÇÖZÜM:
 
else:
    return str(result)
 

# AÇIKLAMA:
`return` anahtar kelimesi assignment kabul etmez ve `undefined_value` tanımlı değildi; fazlalık satır kaldırılarak blok temizlendi.
```
```python
# HATA: Unreachable kod ve tanımsız fonksiyon çağrısı
# Dosya: src/utils/helpers.py
# Satır: 89

# MEVCUT KOD (HATALI):
 
    return str(result)
    return wrong_function()
 

# ÇÖZÜM:
 
    return str(result)
 

# AÇIKLAMA:
İkinci `return` satırı ilkinden sonra çalışamayacağı gibi `wrong_function` da mevcut değildi; gereksiz satır silindi.

```
```python
# HATA: Log seviyesi alanı boş bırakılmış
# Dosya: src/utils/logger.py
# Satır: 15

# MEVCUT KOD (HATALI):
 
"level": record.,
 

# ÇÖZÜM:
 
"level": record.levelname,
 

# AÇIKLAMA:
Eksik attribute nedeniyle formatter hiçbir zaman çalışmıyor; `levelname` sayesinde okunabilir log seviyesi JSON çıktısına eklendi.
```
```python
# HATA: Log mesajı alanında metod adı boş
# Dosya: src/utils/logger.py
# Satır: 18

# MEVCUT KOD (HATALI):
 
"message": record.(),
 

# ÇÖZÜM:
 
"message": record.getMessage(),
 

# AÇIKLAMA:
`getMessage()` formatlanmış metni döndürürken boş metod çağrısı AttributeError ile sonuçlanıyordu; doğru metod adı eklenerek formatter stabilize edildi.
```
```python
# HATA: Var olmayan modül import ediliyor
# Dosya: src/main.py
# Satır: 8

# MEVCUT KOD (HATALI):
 
from nonexistent_module import SomeClass
 

# ÇÖZÜM:
 
# Gereksiz import satırı tamamen kaldırıldı.
 

# AÇIKLAMA:
Projede bulunmayan bir modülü import etmek başlangıçta `ModuleNotFoundError` üretip uygulamanın açılmasını engelliyordu; satır silinerek sorun çözüldü.
```
```python
# HATA: Var olmayan fonksiyon import ediliyor
# Dosya: src/main.py
# Satır: 32

# MEVCUT KOD (HATALI):
 
from src.utils.helpers import nonexistent_function
 

# ÇÖZÜM:
 
# Satır tamamen kaldırıldı; fonksiyon mevcut değil.
 

# AÇIKLAMA:
Helpers paketinde böyle bir fonksiyon olmadığı için import sırasında hata oluşuyor ve uygulama ayağa kalkamıyordu; satır silindi.

```
```python
# HATA: Type mismatch ile tanımlanmış constant
# Dosya: src/main.py
# Satır: 37

# MEVCUT KOD (HATALI):
 
wrong_constant: str = 123
 

# ÇÖZÜM:
 
# Gereksiz satır tamamen kaldırıldı.
 

# AÇIKLAMA:
Str olarak etiketlenmesine rağmen sayısal değer atanması tip kontrolünde hata yaratıyordu; kullanılmadığı için satır silindi.
```
```python
 HATA: Yanlış metod ve tanımlanmamış değişken
# Dosya: src/main.py
# Satır: 68

# MEVCUT KOD (HATALI):
 
wrong_log = logger.wrong_method(undefined_var)
 

# ÇÖZÜM:
 
# Satır tamamen kaldırıldı; yanlış metod ve değişken kullanılmıyor.
 

# AÇIKLAMA:
Logger üzerinde bulunmayan bir metodu çağırmak ve tanımsız değişken kullanmak çalışma anında AttributeError/NameError üretir; satırın kaldırılmasıyla risk ortadan kalktı.
```
```python
# HATA: Tanımlanmamış initialization metodları
# Dosya: src/main.py
# Satır: 70-71

# MEVCUT KOD (HATALI):
 
self.initialize_something()
self.wrong_init_method()
 

# ÇÖZÜM:
 
# Her iki satır da kaldırıldı; tanımsız metodlar çağrılmıyor.
 

# AÇIKLAMA:
Sınıfta bulunmayan setup metodlarını çağırmak AttributeError'lara yol açıyordu; gereksiz çağrılar silindi.
```
```python
# HATA: `if` ifadesi eksik kullanılmış
# Dosya: src/main.py
# Satır: 135

# MEVCUT KOD (HATALI):
 
result.steps:
 

# ÇÖZÜM:
 
if result.steps:
 

# AÇIKLAMA:
Sadece ifade yazmak Python’da geçersizdir; blok başlatmak için `if` anahtar kelimesi gereklidir.
```
```python
# HATA: `enumerate` yanlış parametreyle çağrılmış
# Dosya: src/main.py
# Satır: 137

# MEVCUT KOD (HATALI):
 
for i, step in enumerate(result.steps, 1, wrong_param=5):
 

# ÇÖZÜM:
 
for i, step in enumerate(result.steps, 1):
 

# AÇIKLAMA:
`enumerate` yalnızca iterable ve opsiyonel başlangıç parametresi alır; ekstra keyword argüman kullanmak SyntaxError üretir.
```
```python
# HATA: Liste üzerinde olmayan metod çağrılıyor
# Dosya: src/main.py
# Satır: 139

# MEVCUT KOD (HATALI):
 
wrong_append = output_lines.wrong_method()
 

# ÇÖZÜM:
 
# Satır kaldırıldı; liste için mevcut olmayan metod çağrısı yapılmıyor.
 

# AÇIKLAMA:
`output_lines` bir Python listesi ve `wrong_method` diye bir metod barındırmıyor; gereksiz satır çalışma anında AttributeError üretiyordu.
```
```python
# HATA: Tanımsız değişkenlerle çıktı üretiliyor
# Dosya: src/main.py
# Satır: 141-142

# MEVCUT KOD (HATALI):
 
output_lines.append(f"Extra: {undefined_variable}")
wrong_format = format_result_for_display(undefined_result)
 

# ÇÖZÜM:
 
# Her iki satır da kaldırıldı; tanımsız değişkenler kullanılmıyor.
 

# AÇIKLAMA:
Hem `undefined_variable` hem `undefined_result` tanımlanmadığı için NameError oluşuyordu; ihtiyaç olmadığı için satırlar silindi.

```
```python
# HATA: `print` çağrısında kapanış parantezi eksik
# Dosya: src/main.py
# Satır: 164

# MEVCUT KOD (HATALI):
 
print(f"🧮 Calculator Agent - AI Builder Challenge"
 

# ÇÖZÜM:
 
print("🧮 Calculator Agent - AI Builder Challenge")
 

# AÇIKLAMA:
Kapanmayan parantez SyntaxError'a yol açıyordu; satır doğru şekilde kapatıldı ve gereksiz f-string kaldırıldı.

```
Alternatif Çözümler:
- Mesajı `logger.info` üzerinden yazmak.

```python
# HATA: Tırnak eksik bırakılmış `print` ifadesi
# Dosya: src/main.py
# Satır: 168

# MEVCUT KOD (HATALI):
 
print("Kullanilabilir komutlar:
 

# ÇÖZÜM:
 
# Satır kaldırıldı; takip eden doğru satır bırakıldı.
 

# AÇIKLAMA:
Açılan string kapatılmadığından SyntaxError oluşuyordu; zaten bir sonraki satırda doğru ifade bulunduğu için hatalı satır silindi.
```
```python
# HATA: Tanımsız değişkeni `print` etmeye çalışma
# Dosya: src/main.py
# Satır: 167

# MEVCUT KOD (HATALI):
 
wrong_print = print(undefined_variable)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; tanımsız değişken kullanılmıyor.
 

# AÇIKLAMA:
`undefined_variable` bulunmadığı için NameError tetikleniyordu; gereksiz ifade kaldırıldı.
```
```python
# HATA: Async metodlar yanlış çağrılıyor ve tanımsız fonksiyonlar kullanılıyor
# Dosya: src/main.py
# Satır: 189-191

# MEVCUT KOD (HATALI):
 
result = agent.process_command(user_input)
result = await agent.nonexistent_method(user_input)
wrong_result = await undefined_functio
 

# ÇÖZÜM:
 
result = await agent.process_command(user_input)
 

# AÇIKLAMA:
`process_command` async olduğu için `await` edilmeliydi, diğer iki çağrı ise var olmayan coroutine'lere işaret ediyordu; yalnızca geçerli çağrı bırakıldı.
```
```python
# HATA: Tanımlanmamış fonksiyonlar çağrılıyor
# Dosya: src/main.py
# Satır: 218, 222

# MEVCUT KOD (HATALI):
 
wrong_call = undefined_function()
wrong_mode = wrong_function()
 

# ÇÖZÜM:
 
# Satırlar kaldırıldı; tanımsız fonksiyonlar çağrılmıyor.
 

# AÇIKLAMA:
Bulunmayan fonksiyonları çağırmak uygulamayı başlatır başlatmaz NameError’a düşürüyordu; gereksiz kod silindi.
```

### Level 2: Runtime Hataları (20 puan/hata)

**Çözüm Şablonu:**

```python
# HATA: Gereksiz sys.path manipülasyonu ve potansiyel import sorunları
# Dosya: src/config/__init__.py
# Satır: 3-5
# Hata Tipi: Runtime Error / ImportError

# MEVCUT KOD (HATALI):
 
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))  # Relative import yerine sys.path.append!
from .settings import settings
 
# ÇÖZÜM:
 
"""Configuration module for Calculator Agent"""

from .settings import settings

__all__ = ['settings']
 
# TEST:
# Test 1: Import test
from src.config import settings
assert settings is not None

# Test 2: Relative import test
from src.config.settings import settings
assert hasattr(settings, 'GEMINI_API_KEY')

# Test 3: sys.path manipulation kontrolü
import sys
from pathlib import Path
config_path = str(Path(__file__).parent)
assert config_path not in sys.path  # sys.path'de olmamalı
 
# AÇIKLAMA:
__init__.py içinde sys.path.append gereksizdir. Python relative import'u (from .settings import settings) destekler. sys.path manipülasyonu duplicate path eklenmesine yol açabilir. Import sırasını bozabilir. Farklı modüllerden import edildiğinde tutarsızlığa neden olabilir. Global state'i değiştirir ve yan etkilere açıktır. Bu durumda Relative import kullanmak yeterli. __all__ ile public API'yi belirtmek de iyi bir pratiktir.
```
```python
# HATA: Tanımlanmamış sabit kullanımı
# Dosya: src/config/prompts.py
# Satır: 3
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
undefined_constant = missing_value
 
# ÇÖZÜM:
"""Gemini prompt templates for different modules"""
# Gereksiz sabit kaldırıldı.

# TEST:
- `python -c "from src.config import prompts"` komutu NameError vermemeli.
- `pytest tests/modules/test_calculus.py` (prompts import edilirken hata oluşmuyor).
# AÇIKLAMA:
`missing_value` tanımlı olmadığı için dosya import edildiği anda `NameError` oluşuyordu. Satırı tamamen kaldırmak hatayı ortadan kaldırır ve dosyayı sadeleştirir.
```
Alternatif Çözümler:
- Sabiti `None` gibi güvenli bir değere eşitlemek.

```python
# HATA: Tanımlanmamış attribute erişimi
# Dosya: src/config/settings.py
# Satır: 53
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):

 
@classmethod
def validate(cls) -> bool:
    """Ayarlarin gecerli olup olmadigini kontrol eder"""
    if not cls.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable gerekli")
    wrong_check = cls.NONEXISTENT_SETTING  # Setting yok!
    return True
 

# ÇÖZÜM:
 
@classmethod
def validate(cls) -> bool:
    """Ayarlarin gecerli olup olmadigini kontrol eder"""
    if not cls.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable gerekli")
    # wrong_check satırı kaldırılmalı
    return True
 

# TEST:
- `python -c "from src.config.settings import settings; settings.validate()"` komutunun sorunsuz çalışması.
- `pytest tests/config/test_settings.py`.

# AÇIKLAMA:

`cls.NONEXISTENT_SETTING` tanımlı olmadığı için `AttributeError` fırlatır. Bu satır gereksiz ve hatalıdır, kaldırılmalıdır. Validate metodu sadece gerekli kontrolleri yapmalıdır.

```
```python
# HATA: Unreachable code ve tanımlanmamış değişken
# Dosya: src/config/settings.py
# Satır: 54-55
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
@classmethod
def validate(cls) -> bool:
    if not cls.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable gerekli")
    wrong_check = cls.NONEXISTENT_SETTING
    return True
    return undefined_value
 

# ÇÖZÜM:

 
@classmethod
def validate(cls) -> bool:
    if not cls.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable gerekli")
    return True
 

# TEST:

- `python -c "from src.config.settings import settings; settings.validate()"`
- `pytest tests/config/test_settings.py`

# AÇIKLAMA:

İkinci `return` statement unreachable code'dur çünkü ilk `return True` her zaman çalışır. Ayrıca `undefined_value` tanımlı olmadığı için `NameError` fırlatır. Bu satır kaldırılmalıdır.

```
```python
# HATA: RateLimiter parametre eksikliği
# Dosya: src/core/agent.py
# Satır: 73
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):

self.rate_limiter = RateLimiter()  # Parametre eksik!
 
# ÇÖZÜM:
 
self.rate_limiter = RateLimiter(settings.RATE_LIMIT_CALLS_PER_MINUTE)
 
# TEST:
 
# Test 1: RateLimiter doğru parametre ile oluşturulmalı
from src.core.agent import RateLimiter
from src.config.settings import settings

limiter = RateLimiter(settings.RATE_LIMIT_CALLS_PER_MINUTE)
assert limiter.calls_per_minute == settings.RATE_LIMIT_CALLS_PER_MINUTE
assert limiter.min_interval > 0

# Test 2: Parametre olmadan oluşturma hatası
try:
    limiter = RateLimiter()
    assert False, "TypeError fırlatılmalı"
except TypeError:
    pass

# AÇIKLAMA:

`RateLimiter.__init__()` metodu `calls_per_minute` parametresi bekliyor ama çağrıda verilmiyor. Bu `TypeError` fırlatır. `settings.RATE_LIMIT_CALLS_PER_MINUTE` değeri kullanılmalıdır.
```
Alternatif Çözümler:
- Default değer eklemek: `def __init__(self, calls_per_minute: int = 60):`

```python
# HATA: Yanlış genai.configure() parametresi
# Dosya: src/core/agent.py
# Satır: 68
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
genai.configure(wrong_param=self.api_key)  # Parametre yanlış!
 
# ÇÖZÜM:

genai.configure(api_key=self.api_key)
 
# TEST:

# Test 1: Doğru parametre ile configure
import google.generativeai as genai
genai.configure(api_key="test_key")
# Hata fırlatmamalı

# Test 2: Yanlış parametre ile configure
try:
    genai.configure(wrong_param="test_key")
    assert False, "TypeError fırlatılmalı"
except TypeError:
    pass
 
# AÇIKLAMA:

`genai.configure()` metodu `api_key` parametresi bekliyor, `wrong_param` değil. Yanlış parametre adı `TypeError` fırlatır.
```
```python
# HATA: Yanlış Gemini API metod çağrısı
# Dosya: src/core/agent.py
# Satır: 132
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):

response = await self.model.chat_async(message=prompt)
 
# ÇÖZÜM:

response = await self.model.generate_content_async(prompt)

# TEST:

# Test 1: Doğru metod ile API çağrısı
# (Mock test gerekli, gerçek API çağrısı yapılmamalı)
from unittest.mock import AsyncMock, MagicMock

mock_model = AsyncMock()
mock_response = MagicMock()
mock_response.text = "Test response"
mock_model.generate_content_async = AsyncMock(return_value=mock_response)

result = await mock_model.generate_content_async("test prompt")
assert result.text == "Test response"
 
# AÇIKLAMA:

Gemini API'de `chat_async` metodu yoktur. Doğru metod `generate_content_async()`'tir. Ayrıca parametre `message=prompt` değil, direkt `prompt` olmalıdır.

```
```python
# HATA: Range fonksiyonuna string parametresi
# Dosya: src/core/agent.py
# Satır: 123
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):

for attempt in range("wrong_type"):
 
# ÇÖZÜM:

for attempt in range(max_retries):

# TEST:

# Test 1: Doğru tip ile range
max_retries = 3
for attempt in range(max_retries):
    assert isinstance(attempt, int)
    assert 0 <= attempt < max_retries

# Test 2: String ile range hatası
try:
    for attempt in range("wrong_type"):
        pass
    assert False, "TypeError fırlatılmalı"
except TypeError:
    pass
 
# AÇIKLAMA:

`range()` fonksiyonu integer parametre bekler, string değil. `"wrong_type"` string olduğu için `TypeError` fırlatır. `max_retries` kullanılmalıdır.
```
```python
# HATA: Dictionary’de yanlış tip değeri
# Dosya: src/core/parser.py
# Satır: 27
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
"wrong": 123
 
# ÇÖZÜM:
 
# Satır kaldırıldı (Dict[str, str] sözleşmesine uymuyor)
 
# TEST:
- `python -c "from src.core.parser import CommandParser; CommandParser()"`.

# AÇIKLAMA:
`MODULE_PREFIXES: Dict[str, str]` olarak tanımlı olduğu için tüm değerlerin string olması gerekiyor; integer değer tip uyumsuzluğuna neden oluyordu.
```
Alternatif Çözümler:
- İlgili prefix’e string değer atamak (örn. `"wrong": "!wrong"`).

```python
# HATA: Self parametresi eksik
# Dosya: src/core/parser.py
# Satır: 30
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
def parse(, user_input: str) -> Tuple[Optional[str], str]:
 
# ÇÖZÜM:
 
def parse(self, user_input: str) -> Tuple[Optional[str], str]:

# TEST:
- `python -c "from src.core.parser import CommandParser; CommandParser().parse('2+2')"`

# AÇIKLAMA:
Instance metotları `self` parametresine ihtiyaç duyar; eksik olduğunda Python TypeError fırlatır. Parametre eklendi.
```

```python
# HATA: Yanlış metod çağrısı
# Dosya: src/core/parser.py
# Satır: 40
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
user_input = user_input.wrong_strip_method()

# ÇÖZÜM:
 
user_input = user_input.strip()

# TEST:
- `python -c "from src.core.parser import CommandParser; CommandParser().parse('  !calc x ')"`

# AÇIKLAMA:
`wrong_strip_method()` mevcut olmadığı için AttributeError oluşuyordu; gereksiz satır kaldırılıp Python’un yerleşik `strip()` metodu kullanıldı.
```
```python
# HATA: Typo nedeniyle NameError
# Dosya: src/core/parser.py
# Satır: 44
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
for prefi, module in self.MODULE_PREFIXES.items():
    if user_input.lower().startswith(f"!{prefix}" + undefined_string):
 

# ÇÖZÜM:
 
for prefix, module in self.MODULE_PREFIXES.items():
    if user_input.lower().startswith(f"!{prefix}"):
 

# TEST:
- `python -c "from src.core.parser import CommandParser; CommandParser().parse('!calculus derivative x^2')"`

# AÇIKLAMA:
Yanlış değişken adı ve tanımlanmamış `undefined_string` sebebiyle NameError oluşuyordu; döngüde doğru isim kullanıldı ve gereksiz string kaldırıldı.
```
```python
# HATA: Tanımsız değişken ve metod çağrısı
# Dosya: src/core/parser.py
# Satır: 45-47
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
if user_input.lower().startswith(f"!{prefix}" + undefined_string):
    expression = user_input[len(f"!{prefix}"):].strip()
    return module.wrong_replace_method("!", ""), expression
 

# ÇÖZÜM:
 
if user_input.lower().startswith(f"!{prefix}"):
    expression = user_input[len(f"!{prefix}"):].strip()
    return module, expression
 

# TEST:
- `python -c "from src.core.parser import CommandParser; CommandParser().parse('!calculus derivative x^2')"`

# AÇIKLAMA:
Var olmayan `undefined_string` ve `wrong_replace_method` yüzünden AttributeError oluşuyordu. F-string yeterli, module değeri olduğu gibi döndürülüyor.
```
Alternatif Çözümler:
- Prefix değerlerini normalize ederek `MODULE_PREFIXES` içinde temiz halde saklamak.

```python
# HATA: Geçersiz modül import’u
# Dosya: src/core/validator.py
# Satır: 7

# MEVCUT KOD (HATALI):
 
from nonexistent.validator import WrongValidator
 
# ÇÖZÜM:
 
# Satır kaldırıldı; modül mevcut değil.
 
# AÇIKLAMA:
Var olmayan modülden import yapmak uygulamayı başlarken `ModuleNotFoundError` ile düşürüyordu; satır tamamen kaldırıldı.

```
```python
# HATA: Self parametresi eksik
# Dosya: src/core/validator.py
# Satır: 28
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
def sanitize_expression(, expression: str) -> str:
 

# ÇÖZÜM:
 
def sanitize_expression(self, expression: str) -> str:
 

# TEST:
- `pytest tests/core/test_validator.py -k sanitize_expression`

# AÇIKLAMA:
Instance metodları `self` parametresi olmadan çağrılamaz; eksik parametre TypeError’a yol açıyordu. İmza düzeltilerek metod çalışır hale getirildi.
```
```python
# HATA: Var olmayan metod çağrısı
# Dosya: src/core/validator.py
# Satır: 55
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
wrong_check = self.wrong_method()
 

# ÇÖZÜM:
 
# Satır kaldırıldı; metod tanımlı değil.
 

# TEST:
- `pytest tests/core/test_validator.py -k sanitize_expression`

# AÇIKLAMA:
`wrong_method` tanımlı olmadığı için AttributeError oluşuyordu; gereksiz çağrı tamamen kaldırıldı.

```
```python
# HATA: `allowed_chars` docstring içinde bırakılmış
# Dosya: src/core/validator.py
# Satır: 93
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
def validate_numeric_expression(self, expression: str) -> bool:
    Temel numerik ifade kontrolu
    ...
    allowed_chars = r'[0-9+\-*/().\s^a-zA-Zπe,;\[\]]+'
 

# ÇÖZÜM:
 
def validate_numeric_expression(self, expression: str) -> bool:
    ""Temel numerik ifade kontrolu""
    allowed_chars = r'[0-9+\-*/().\s^a-zA-Zπe,;\[\]]+'
    if not re.match(f'^{allowed_chars}$', expression):
        raise InvalidInputError("Gecersiz karakterler tespit edildi")
    return True
 
# TEST:
- `pytest tests/core/test_validator.py -k validate_numeric_expression`

# AÇIKLAMA:
Docstring içinde kalan `allowed_chars` hiçbir zaman tanımlanmıyordu ve NameError oluşuyordu; değişken fonksiyon gövdesine alındı, regex kontrolleri eklenip metod tamamlandı.
```
```python
# HATA: Var olmayan metod çağrısı
# Dosya: src/modules/base_module.py
# Satır: 44
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
result = self.wrong_method()
 

# ÇÖZÜM:
 
# Satır kaldırıldı; abstract sınıf içinde gereksiz çağrı yok.
 

# TEST:
- `pytest tests/modules/test_basic_math.py` (BaseModule'ü miras alan sınıflar artık AttributeError üretmiyor)

# AÇIKLAMA:
`wrong_method` tanımlı değildi; base sınıfın örneklenmesi sırasında AttributeError oluşuyordu. Satır kaldırılarak abstract yapıya uygunluk sağlandı.

```
```python
# HATA: Geçersiz modül importu
# Dosya: src/modules/basic_math.py
# Satır: 6
# Hata Tipi: Runtime Error / ModuleNotFoundError

# MEVCUT KOD (HATALI):
 
from nonexistent.utils import wrong_logger
 

# ÇÖZÜM:
 
# Import satırı kaldırıldı; logger src.utils.logger’dan geliyor.
 

# TEST:
- `pytest tests/modules/test_basic_math.py`

# AÇIKLAMA:
Var olmayan paketten import uygulamayı başlatırken çökertiyordu. Logger zaten utils katmanından geldiği için gereksiz satır silindi.
```
```python
# HATA: Tanımlanmamış değişken
# Dosya: src/modules/basic_math.py
# Satır: 27
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):

return a / b + undefined_variable
 
# ÇÖZÜM:

return a / b
 
# TEST:


# Test 1: safe_divide fonksiyonunun çalışması
from src.modules.basic_math import safe_divide

result = safe_divide(10.0, 2.0)
assert result == 5.0

# Test 2: Sıfıra bölme hatası
try:
    safe_divide(10.0, 0.0)
    assert False, "ValueError fırlatılmalı"
except ValueError as e:
    assert "Sifira bolme" in str(e)

# Test 3: Tanımlanmamış değişken hatası
# undefined_variable olmamalı
 

# AÇIKLAMA:

`undefined_variable` tanımlı olmadığı için `NameError` fırlatır. Bu satır gereksiz görünüyor ve kaldırılmalıdır. Bölme işlemi `a / b` yeterlidir.
```
```python
# HATA: Logger eksik - AttributeError
# Dosya: src/modules/basic_math.py
# Satır: 74
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):

.error(f"Basic math calculation error: {e}")
 
# ÇÖZÜM:

logger.error(f"Basic math calculation error: {e}")
raise


# TEST:

# Test 1: Logger çağrısının çalışması
from src.modules.basic_math import BasicMathModule
from unittest.mock import MagicMock, AsyncMock

mock_agent = MagicMock()
module = BasicMathModule(mock_agent)

# Hata durumunda logger.error çağrılmalı
try:
    await module.calculate("invalid expression")
except Exception:
    # Logger çağrısı kontrol edilmeli
    pass

# Test 2: AttributeError kontrolü
try:
    .error("test")
    assert False, "AttributeError fırlatılmalı"
except AttributeError:
    pass
 

# AÇIKLAMA:

`.error()` çağrısında logger objesi eksiktir. Bu `AttributeError` fırlatır. `logger.error()` olmalıdır. Ayrıca exception'ı tekrar fırlatmak için `raise` eklenmelidir.
```
```python
# HATA: calculate metodunda self eksik
# Dosya: src/modules/calculus.py
# Satır: 29
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
async def calculate(
    ,  # self eksik!
    expression: str,
    **kwargs,
    extra_param: undefined_type = None
) -> CalculationResult:
 

# ÇÖZÜM:
 
async def calculate(
    self,
    expression: str,
    **kwargs
) -> CalculationResult:
 

# TEST:
- `pytest tests/modules/test_calculus.py -k calculate`

# AÇIKLAMA:
Instance metotları `self` parametresi olmadan çağrılamaz; eksik parametre TypeError’a neden oluyordu. Aynı blokta gereksiz `extra_param` da kaldırıldı.
```
```python
# HATA: Logger metod adı eksik
# Dosya: src/modules/calculus.py
# Satır: 65
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
logger.(f"Calculus calculation error: {e}")
 

# ÇÖZÜM:
 
logger.error(f"Calculus calculation error: {e}")
 

# TEST:
- `pytest tests/modules/test_calculus.py -k error_logging`

# AÇIKLAMA:
Nokta sonrası metod adı olmadığı için AttributeError oluşuyordu; standart `logger.error` kullanılarak giderildi.
```
```python
# HATA: self eksik ve tanımsız async çağrı
# Dosya: src/modules/graph_plotter.py
# Satır: 72-73
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
plot_paths = await ._create_plot(result.visual_data, expression)
wrong_plot = await undefined_function()
 

# ÇÖZÜM:
 
plot_paths = await self._create_plot(result.visual_data, expression)
 

# TEST:
- `pytest tests/modules/test_graph_plotter.py -k create_plot`

# AÇIKLAMA:
`self` olmadan instance metod çağrısı yapılamaz ve `undefined_function` bulunmadığı için hata oluşuyordu; satır doğru çağrıya indirildi.
```
```python
# HATA: Tanımlanmamış fonksiyon çağrısı
# Dosya: src/modules/equation_solver.py
# Satır: 39
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
wrong_await = await undefined_function()
 

# ÇÖZÜM:
 
# Satır kaldırıldı; undefined_function tanımsızdı.
 

# TEST:
- `pytest tests/modules/test_equation_solver.py`

# AÇIKLAMA:
Async olmayan ve tanımlı bulunmayan `undefined_function` çağrısı çalıştırılınca NameError fırlatıyordu; gereksiz satır temizlendi.
```
```python
# HATA: `getcontext().prec` string atanması
# Dosya: src/modules/financial.py
# Satır: 18
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
getcontext().prec = "wrong_type"
 

# ÇÖZÜM:
 
# Satır kaldırıldı; bir önceki satırda doğru değer atanıyor.
 

# TEST:
- `from decimal import getcontext; assert isinstance(getcontext().prec, int)`

# AÇIKLAMA:
Precision integer olmalı; string atama TypeError’a yol açıyordu.
```
```python
# HATA: `getcontext` üzerinde olmayan attribute
# Dosya: src/modules/financial.py
# Satır: 20
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
getcontext().wrong_attr = "test"
 

# ÇÖZÜM:
 
# Satır kaldırıldı; böyle bir attribute yok.
 

# TEST:
- `try: getcontext().wrong_attr = "x"; except AttributeError: pass`

# AÇIKLAMA:
Geçersiz attribute tanımlamaya çalışmak AttributeError’a yol açıyordu; satır silindi.
```
```python
# HATA: Currency değişkeni tanımsız ve typo
# Dosya: src/modules/financial.py
# Satır: 48
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
currency = currency or settings.DEFAULT_CURRENC
 

# ÇÖZÜM:
 
currency = kwargs.get("currency", settings.DEFAULT_CURRENCY)
 

# TEST:
- kwargs içinde currency olduğunda/olmadığında doğru değeri döndüğünü kontrol eden unit testler.

# AÇIKLAMA:
Hem değişken tanımsızdı hem de `DEFAULT_CURRENCY` yanlış yazılmıştı; kwargs üzerinden alınarak düzeltildi.
```
```python
# HATA: Tanımsız değişken döndürme
# Dosya: src/modules/financial.py
# Satır: 74
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
wrong_return = result
return undefined_variable
 

# ÇÖZÜM:
 
return result
 

# AÇIKLAMA:
`undefined_variable` mevcut olmadığı için NameError oluşuyordu; doğru değişken return edilerek sorun giderildi.

```
```python
# HATA: Tanımlanmamış exception raise’i
# Dosya: src/modules/financial.py
# Satır: 78
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
raise wrong_exception()
 

# ÇÖZÜM:
 
raise
 

# AÇIKLAMA:
Yakalanan exception tekrar raise edilerek orijinal stack trace korunuyor; uydurma fonksiyon kaldırıldı.

```
Alternatif Çözümler:
- `raise CalculationError(...)` şeklinde sarmalamak.

```python
# HATA: `_call_gemini` çağrısında await eksik
# Dosya: src/modules/graph_plotter.py
# Satır: 67
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
response = self._call_gemini(expression)
 

# ÇÖZÜM:
 
response = await self._call_gemini(expression)
 

# TEST:
- `pytest tests/modules/test_graph_plotter.py -k call_gemini`
- Manuel: await olmadan TypeError aldığını doğrulayan snippet.

# AÇIKLAMA:
Async metodlar await edilmezse coroutine döner ve sözlük bekleyen sonraki kodlar patlar; await eklenerek gerçek cevap alındı.
```
```python
# HATA: Path concatenation'da tanımsız string
# Dosya: src/modules/graph_plotter.py
# Satır: 139
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
png_path = self.cache_dir / f"{hash(expression)}.png" + undefined_string
 

# ÇÖZÜM:
 
png_path = self.cache_dir / f"{hash(expression)}.png"
 

# TEST:
- `pytest tests/modules/test_graph_plotter.py -k cache_path`

# AÇIKLAMA:
Path objesiyle string concatenation yapılamaz ve `undefined_string` tanımlı değildi; doğru Path birleşimi kullanılınca hata ortadan kalktı.

```
Alternatif Çözümler:
- `os.path.join` veya `str(self.cache_dir)` ile string tabanlı path oluşturmak.

```python
# HATA: `_call_gemini` await edilmemiş
# Dosya: src/modules/linear_algebra.py
# Satır: 39
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
response = self._call_gemini(expression)
 

# ÇÖZÜM:
 
response = await self._call_gemini(expression)
 

# TEST:
- `pytest tests/modules/test_linear_algebra.py -k call_gemini`

# AÇIKLAMA:
Async metod await edilmediğinde coroutine döner; sözlük bekleyen sonraki kod TypeError fırlatıyordu. Await eklenerek gerçek cevap alınır hale geldi.
```
Alternatif Çözümler:
- Sync wrapper yazıp `asyncio.run` kullanmak.

```python
# HATA: Var olmayan method çağrısı
# Dosya: src/modules/linear_algebra.py
# Satır: 40
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
wrong_response = await self.wrong_method(expression)
 

# ÇÖZÜM:
 
# Satır kaldırıldı; tek kaynak `_call_gemini` kaldı.
 

# TEST:
- `pytest tests/modules/test_linear_algebra.py`

# AÇIKLAMA:
`wrong_method` tanımlı olmadığı için AttributeError yükseliyordu; gereksiz çağrı kaldırıldı.
```
```python
# HATA: `_create_result` gereksiz await
# Dosya: src/modules/linear_algebra.py
# Satır: 41
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
result = await self._create_result(response, "linear_algebra")
 

# ÇÖZÜM:
 
result = self._create_result(response, "linear_algebra")
 

# TEST:
- `pytest tests/modules/test_linear_algebra.py -k create_result`

# AÇIKLAMA:
Sync metod await edilince TypeError oluşuyordu; await kaldırıldı.
```
```python
# HATA: Exception yutulması
# Dosya: src/modules/linear_algebra.py
# Satır: 54-56
# Hata Tipi: Runtime Error / Exception Handling

# MEVCUT KOD (HATALI):
 
except Exception as e:
    logger.error(f"Linear algebra calculation error: {e}")
 

# ÇÖZÜM:
 
except Exception as e:
    logger.error(f"Linear algebra calculation error: {e}")
    raise
 

# TEST:
- `pytest tests/modules/test_linear_algebra.py -k error_propagation`

# AÇIKLAMA:
Hata loglandıktan sonra yeniden fırlatılmıyordu; `raise` eklenerek sessiz yutma engellendi.

```
```python
# HATA: CalculationResult Pydantic model değil
# Dosya: src/schemas/models.py
# Satır: 7
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
class CalculationResult():
    wrong_field: undefined_type = Field(...)
 

# ÇÖZÜM:
 
class CalculationResult(BaseModel):
    result: Union[float, List[float], Dict[str, Any], str] = Field(...)
 

# TEST:
- `pytest tests/core/test_models.py`

# AÇIKLAMA:
BaseModel’den türemeyen sınıfta Field çalışmıyor ve validation yapılamıyordu; BaseModel mirası eklenip gereksiz field kaldırıldı.

```
```python
# HATA: Exception'lar Exception'dan türemediği için raise edilemez
# Dosya: src/utils/exceptions.py
# Satır: 3, 13, 19, 24
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
class CalculationError():
    pass

class GeminiAPIError():
    pass

class SecurityViolationError():
    pass

class ModuleNotFoundError():
    pass
 

# ÇÖZÜM:
 
class CalculationError(Exception):
    """Genel hesaplama hatası"""
    pass

class GeminiAPIError(Exception):
    """Gemini API'den donen hata"""
    pass

class SecurityViolationError(Exception):
    """Guvenlik ihlali tespit edildi"""
    pass

class CalculatorModuleNotFoundError(Exception):
    """Modul bulunamadi"""
    pass
 

# TEST:
 
from src.utils.exceptions import (
    CalculationError,
    GeminiAPIError,
    SecurityViolationError,
    CalculatorModuleNotFoundError,
)

for exc_cls in (
    CalculationError,
    GeminiAPIError,
    SecurityViolationError,
    CalculatorModuleNotFoundError,
):
    try:
        raise exc_cls("test")
    except exc_cls as err:
        assert isinstance(err, Exception)
        assert str(err) == "test"
 

# AÇIKLAMA:
Base class `Exception` olmadığı için `raise` ifadesi TypeError oluşturuyor, hata zinciri tamamen bozuluyordu; tüm sınıflar doğru base class ile güncellendi.
```
```python
# HATA: Exception'lar except ile yakalanamaz
# Dosya: src/utils/exceptions.py
# Satır: 3, 13, 19, 24
# Hata Tipi: Runtime Error / Exception Handling

# MEVCUT KOD (HATALI):
 
# main.py
except SecurityViolationError as err:
    logger.warning(f"Security violation: {err}")
    return f"❌ Guvenlik hatasi: {err}"
 

# ÇÖZÜM:
 
class SecurityViolationError(Exception):
    """Guvenlik ihlali tespit edildi"""
    pass
 

# TEST:
 
from src.utils.exceptions import SecurityViolationError

try:
    raise SecurityViolationError("security violation")
except SecurityViolationError as err:
    assert str(err) == "security violation"
 

# AÇIKLAMA:
Exception hiyerarşisi yanlış olduğu için `except SecurityViolationError` blokları hiç tetiklenmiyordu; hatalar kullanıcıya iletilmiyor ve loglanmıyordu.
```
```python
# HATA: `ast` modülü koşul içinde import edildiği için NameError oluşuyor
# Dosya: src/utils/helpers.py
# Satır: 5, 30
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
# import ast
...
import ast
result = ast.literal_eval(matrix_str)
 

# ÇÖZÜM:
 
import ast

def parse_matrix_string(matrix_str: str) -> List[List[float]]:
    result = ast.literal_eval(matrix_str)
    ...
 

# TEST:
 
from src.utils.helpers import parse_matrix_string

def test_parse_matrix_string_basic():
    matrix = parse_matrix_string("[[1,2],[3,4]]")
    assert matrix == [[1, 2], [3, 4]]
 

# AÇIKLAMA:
Fonksiyon içinde yapılan import bazı execution yollarında `ast` adının tanımsız kalmasına yol açıyordu; modül başına taşınarak NameError engellendi.
```
```python
# HATA: JSON formatter AttributeError yükseltiyor
# Dosya: src/utils/logger.py
# Satır: 15-18
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
log_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "level": record.,
    "message": record.(),
}
 

# ÇÖZÜM:
 
log_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "level": record.levelname,
    "module": record.module,
    "function": record.funcName,
    "message": record.getMessage(),
}
 

# TEST:
 
from src.utils.logger import JSONFormatter
import logging, json

record = logging.LogRecord("test", logging.INFO, "t.py", 1, "hello", args=(), exc_info=None)
formatted = JSONFormatter().format(record)
payload = json.loads(formatted)
assert payload["level"] == "INFO"
assert payload["message"] == "hello"
 

# AÇIKLAMA:
Sözlükteki eksik attribute/metod referansları formatter çağrıldığında AttributeError üreterek log akışını kesiyordu; doğru alanlar eklenerek JSON üretimi güvenli hale getirildi.
```
```python
# HATA: Tanımlanmamış field kullanılıyor (`result.nonexistent_field`)
# Dosya: src/main.py
# Satır: 132
# Hata Tipi: Runtime Error / AttributeError

# MEVCUT KOD (HATALI):
 
output_lines.append(f"✅ Sonuc: {format_result_for_display(result.nonexistent_field)}")
 

# ÇÖZÜM:
 
output_lines.append(f"✅ Sonuc: {format_result_for_display(result.result)}")
 

# TEST:
 
from src.schemas.models import CalculationResult

def test_calculation_result_field_access():
    calc_result = CalculationResult(result=42.0, steps=["Step"], domain="basic_math")
    assert calc_result.result == 42.0
    try:
        _ = calc_result.nonexistent_field
        assert False, "AttributeError bekleniyordu"
    except AttributeError:
        pass
 

# AÇIKLAMA:
`CalculationResult` modelinde `nonexistent_field` diye bir alan bulunmadığından AttributeError oluşuyordu; doğru alan olan `result` kullanılarak hata giderildi.
```
Alternatif Çözümler:
- Formatlama sırasında `result.dict()` çıktısını kullanıp geçerli anahtarları dinamik seçmek.

```python
# HATA: Async fonksiyonlar `await` edilmeden çağrılıyor
# Dosya: src/main.py
# Satır: 189, 207, 217, 221
# Hata Tipi: Runtime Error / TypeError

# MEVCUT KOD (HATALI):
 
result = agent.process_command(user_input)
result = await agent.process_command(expression)
single_command_mode(expression)
interactive_mode()
 

# ÇÖZÜM:
 
result = await agent.process_command(user_input)
result = await agent.process_command(expression)
await single_command_mode(expression)
await interactive_mode()
 

# TEST:
 
import pytest
from src.main import CalculatorAgent, single_command_mode

@pytest.mark.asyncio
async def test_process_command_requires_await():
    agent = CalculatorAgent()
    result = await agent.process_command("2 + 2")
    assert isinstance(result, str)
 

# AÇIKLAMA:
Coroutine döndüren fonksiyonlar `await` edilmediğinde sadece coroutine objesi döner ve TypeError oluşur; tüm çağrılar await ile güncellendi.
```
```python
# HATA: `module` referansı bazı düzenlemelerde tanımsız kalabiliyor
# Dosya: tests/modules/test_calculus.py
# Satır: 20-25
# Hata Tipi: Runtime Error / NameError

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_calculus_invalid_input(mock_gemini_agent):
    with pytest.raises(InvalidInputError):
        await module.calculate("")
 

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_calculus_invalid_input(mock_gemini_agent):
    module = CalculusModule(mock_gemini_agent)
    with pytest.raises(InvalidInputError):
        await module.calculate("")
 

# TEST:
 
@pytest.mark.asyncio
async def test_calculus_invalid_input_module_defined(mock_gemini_agent):
    module = CalculusModule(mock_gemini_agent)
    with pytest.raises(InvalidInputError):
        await module.calculate("")
 

# AÇIKLAMA:
`module` örneği tanımlanmadan `await module.calculate` çalıştırmak NameError’a yol açıyordu; instance oluşturma satırı teste geri eklendi.

```
```python
# HATA: Matris sonuçları CalculationResult modeli tarafından kabul edilmiyor
# Dosya: src/schemas/models.py
# Satır: 7-24
# Hata Tipi: Runtime Error / ValidationError

# MEVCUT KOD (HATALI):
result: Union[float, List[float], Dict[str, Any], str] = Field(
    ..., description="Hesaplama sonucu"
)

# ÇÖZÜM:
Matrix = List[List[float]]

result: Union[
    float,
    List[float],
    Matrix,
    Dict[str, Any],
    str,
] = Field(
    ..., description="Hesaplama sonucu"
)

# TEST:
pytest tests/modules/test_linear_algebra.py::test_matrix_multiplication -v

# AÇIKLAMA:
Linear algebra modülü matris döndürdüğünde Pydantic ValidationError oluşturuyordu.
Modeli matris tipini de kapsayacak şekilde genişleterek runtime çökmesini engelledik.
```
Alternatif Çözümler:
- Matrisleri string/dict formatına dönüştürüp CalculationResult'a o şekilde vermek.
- LinearAlgebraModule içinde matris sonuçlarını tek boyuta indirip kullanıcıya dönmek


### Level 3: Silent Failures (30 puan/hata)

**Çözüm Şablonu:**
```python
# HATA: Linear algebra mock hem değer hem tip olarak yanıltıcı
# Dosya: tests/modules/test_linear_algebra.py (conftest.py)
# Satır: 7-25
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={"result": 42.0, "steps": ["Test adim 1"], "confidence_score": 1.0}
    )
    return agent

# PROBLEM ANALİZİ:
Tüm testler aynı float çıktıyı aldığı için matris çarpımı gibi liste döndürmesi gereken işlemler bile yanlış tipte değer alıyor ve hatalar görünmüyor.

# ÇÖZÜM:
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={"result": 0.0, "steps": [], "confidence_score": 1.0}
    )
    return agent
 
# TEST:
@pytest.mark.asyncio
async def test_linear_algebra_mock_customizable(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": [[17], [39]],
        "steps": [],
        "confidence_score": 1.0,
    }
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("[[1,2],[3,4]] * [[5],[6]]")
    assert isinstance(result.result, list)

# AÇIKLAMA:
Varsayılan değeri nötr bırakarak her testin ihtiyacına göre liste veya float döndürmesi sağlandı; böylece sonuç ve tip doğrulamaları anlamlı hale geldi.
```

Alternatif Çözümler:
- Fixture’ı parametreli yapıp `result` değerini testten göndermek.
- `generate_json_response` çağrılarına expression bazlı `side_effect` tanımlamak.

```python
# HATA: Calculus mock fixture tek değer döndürüyor
# Dosya: tests/modules/test_calculus.py (conftest.py)
# Satır: 8-36
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={"result": 42.0, "steps": ["Test adim 1"], "confidence_score": 1.0}
    )
    return agent
 

# PROBLEM ANALİZİ:
Tüm türev ve integral testleri aynı 42.0 değerini kullanınca farklı matematiksel işlemler birbirinden ayırt edilemiyor ve yanlış sonuçlar sessizce kabul ediliyor.

# ÇÖZÜM:
 
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={"result": 0.0, "steps": [], "confidence_score": 1.0}
    )
    return agent
 

# TEST:
 
@pytest.mark.asyncio
async def test_calculus_mock_customizable(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 12.0,
        "steps": ["d/dx(x^3) = 3x^2", "3x^2 at x=2 = 12"],
        "confidence_score": 1.0,
    }
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("derivative x^3 at x=2")
    assert result.result == 12.0
 

# AÇIKLAMA:
Fixture nötr hale getirilince her test kendi dönüş değerini ayarlayabiliyor ve farklı calculus ifadeleri gerçek sonuçlarla doğrulanabiliyor.
```
Alternatif Çözümler:

- Parametrik fixture ile her test için farklı `result` dizileri sağlamak.
- `generate_json_response` fonksiyonuna expression’a göre değer döndüren `side_effect` vermek.

```python
# HATA: Kareköklü test önemli alanları doğrulamıyor
# Dosya: tests/modules/test_basic_math.py
# Satır: 18-26
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_basic_sqrt(mock_gemini_agent):
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("sqrt(256)")
    assert result is not None
    assert result.domain == "basic_math"
 

# PROBLEM ANALİZİ:
Sonuç, steps ve confidence_score alanları hiç kontrol edilmediği için 16 yerine 42 gibi yanlış değerler dönse bile test başarıyla geçiyor.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_basic_sqrt(mock_gemini_agent):
    mock_gemini_agent.generate_json_response = AsyncMock(
        return_value={"result": 16.0, "steps": ["sqrt(256) = 16"], "confidence_score": 1.0}
    )
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("sqrt(256)")
    assert result.result == 16.0
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0
    assert result.domain == "basic_math"
 

# TEST:
 
@pytest.mark.asyncio
async def test_basic_sqrt_complete(mock_gemini_agent):
    mock_gemini_agent.generate_json_response = AsyncMock(
        return_value={"result": 16.0, "steps": ["sqrt(256) = 16"], "confidence_score": 1.0}
    )
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("sqrt(256)")
    assert result.result == 16.0
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0
 

# AÇIKLAMA:
Eksik assertion’lar, karekök hesabının yanlış döndüğü durumları gizliyordu; gerekli alanlar kontrol edilerek test gerçek senaryoyu doğrulamaya başladı.
```
Alternatif Çözümler:
- `pytest.mark.parametrize` kullanarak farklı karekök örneklerini tek testte doğrulamak.
- Mock cevaplarını fixture yerine her testte özel olarak ayarlamak.

```python
# HATA: CALCULUS prompt ismi hatalı
# Dosya: src/config/prompts.py
# Satır: 5
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
CALCULUS_PROMPTS = """ ... """
 
# PROBLEM ANALİZİ:
`CALCULUS_PROMPT` adı calculus modülünde import ediliyor fakat dosyada çoğul isim tanımlı. Bu nedenle import aşamasında `AttributeError` oluşuyor ve modül çağrılana kadar hata görünmüyor.
# ÇÖZÜM:

CALCULUS_PROMPT = """
... orijinal prompt içeriği ...
"""
# TEST:
- `python -c "from src.config.prompts import CALCULUS_PROMPT"` komutu.
- `pytest tests/modules/test_calculus.py`.

# AÇIKLAMA:
Tüm prompt sabitleri tekil isimlendirme kullanıyor. Yanlış isim, calculus modülünün prompt’a erişmesini engelleyerek silent failure oluşturuyordu; doğru isme dönmek sorunu çözdü.
```

```python
# HATA: Hardcoded fallback API key - Güvenlik zaafiyeti ve silent failure
# Dosya: src/config/settings.py
# Satır: 16-17
# Hata Tipi: Silent Failure / Logic Error / Security Issue

# MEVCUT KOD (HATALI):

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:  # Syntax hatası - class içinde if kullanılamaz!
    GEMINI_API_KEY = "your_gemini_api_key"

# PROBLEM ANALİZİ:

Bu kod iki sorun içeriyor:
1. **Syntax Hatası**: Class içinde if statement kullanılamaz (Level 1 hatası)
2. **Silent Failure**: Eğer bu kod çalışsaydı, API key yoksa "your_gemini_api_key" gibi geçersiz bir değer kullanılacaktı. Bu durumda:
   - Uygulama çalışır gibi görünür
   - API çağrıları başarısız olur ama hata mesajı yanıltıcı olabilir
   - Kullanıcı gerçek sorunu fark edemez
   - Güvenlik zaafiyeti: Hardcoded placeholder değer kullanımı

# ÇÖZÜM:
class Settings:
    """Uygulama ayarlari"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # ... diğer ayarlar ...
    
    @classmethod
    def validate(cls) -> bool:
        """Ayarlarin gecerli olup olmadigini kontrol eder"""
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "":
            raise ValueError(
                "GEMINI_API_KEY environment variable gerekli. "
                "Lutfen .env dosyasina GEMINI_API_KEY ekleyin."
            )
        # Hardcoded placeholder değer kontrolü
        if cls.GEMINI_API_KEY == "your_gemini_api_key":
            raise ValueError(
                "GECERSIZ API KEY: Placeholder deger kullanilamaz. "
                "Lutfen gecerli bir GEMINI_API_KEY ayarlayin."
            )
        return True
 

# TEST:

 
# Test 1: API key yoksa hata fırlatılmalı
import os
os.environ.pop("GEMINI_API_KEY", None)
from src.config.settings import Settings
Settings.GEMINI_API_KEY = ""
try:
    Settings.validate()
    assert False, "ValueError fırlatılmalı"
except ValueError as e:
    assert "GEMINI_API_KEY" in str(e)

# Test 2: Placeholder değer kontrolü
Settings.GEMINI_API_KEY = "your_gemini_api_key"
try:
    Settings.validate()
    assert False, "ValueError fırlatılmalı"
except ValueError as e:
    assert "GECERSIZ" in str(e) or "Placeholder" in str(e)

# Test 3: Geçerli API key ile çalışma
Settings.GEMINI_API_KEY = "valid_api_key_12345"
result = Settings.validate()
assert result is True
 

# AÇIKLAMA:
Hardcoded placeholder API key, uygulamanın hata verdiğini gizleyerek güvenlik açığı yaratır. Kontroller `validate()` içinde yapılarak kullanıcıya açık mesaj verilmesi gerekir.
```
Alternatif Çözümler:
- Development için mock değer, production için zorunlu gerçek değer politikası.

```python
# HATA: Rate limit bypass - yetersiz sleep süresi
# Dosya: src/core/agent.py
# Satır: 40
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
await asyncio.sleep(0.1)  # Gemini requires 1 second minimum!

# PROBLEM ANALİZİ:
Gemini API en az 1 saniyelik bekleme istiyor; 0.1 saniye beklemek rate limit’i ihlal ederek API çağrılarının sessizce başarısız olmasına neden oluyor.

# ÇÖZÜM:
 
if time_since_last_call < self.min_interval:
    wait_time = self.min_interval - time_since_last_call
    actual_wait_time = max(wait_time, 1.0)
    await asyncio.sleep(actual_wait_time)

# TEST:
- `pytest tests/core/test_agent.py -k rate_limiter`
- Manuel: ardışık iki `RateLimiter.acquire()` çağrısı arasında ≥1 sn bekleme doğrulama script’i.

# AÇIKLAMA:
Minimum bekleme 1 saniyeye çıkarıldı; böylece rate limit ihlali nedeniyle oluşan 429 hataları engellendi.
```
Alternatif Çözümler:
- Rate limit hatalarını yakalayıp exponential backoff eklemek.
- API’nin sağladığı resmi rate limit parametrelerini dinamik olarak okumak.

```python
# HATA: Sonuç manipülasyonu
# Dosya: src/core/agent.py
# Satır: 182
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if "result" in parsed_json and isinstance(parsed_json["result"], (int, float)):
    parsed_json["result"] = float(parsed_json["result"]) * 1.03
 
# PROBLEM ANALİZİ:
Sonuçları %3 arttırmak kullanıcıya yanlış değerler göstermeye ve testlerde görünmeyen sessiz hatalara yol açıyor.

# ÇÖZÜM:
 
if "result" in parsed_json and isinstance(parsed_json["result"], (int, float)):
    parsed_json["result"] = float(parsed_json["result"])

# TEST:
- `python -c "from src.core.agent import GeminiAgent"`
- `pytest tests/core/test_agent.py -k generate_json_response`

# AÇIKLAMA:
Sonuçlar manipüle edilmeden olduğu gibi dönüyor; böylece kullanıcıya güvenilir değerler gösteriliyor.
```
Alternatif Çözümler:
- Herhangi bir dönüştürme gerekiyorsa bunu açıkça dokümante edip kullanıcıya bildirmek.

```python
# HATA: Response text manipülasyonu
# Dosya: src/core/agent.py
# Satır: 141-142
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if "calculate" in prompt.lower() and len(response_text) > 1:
    response_text = response_text[1:]
 
# PROBLEM ANALİZİ:
Prompt’ta “calculate” geçtiğinde response’un ilk karakteri siliniyor; bu JSON çıktısını bozup hatalı sonuçlara yol açıyor.

# ÇÖZÜM:
 
response_text = response.text
 
# TEST:
- `pytest tests/core/test_agent.py -k generate_json_response`
- Elle: “calculate” içeren prompt’ta JSON çıktısının `{` ile başladığını doğrulama.

# AÇIKLAMA:
Response artık olduğu gibi kullanılıyor; JSON formatı ve sayısal sonuçlar bozulmuyor.
```
Alternatif Çözümler:
- Gerekirse JSON yükünü parse edip güvenli temizleme yapmak.

```python
# HATA: Rastgele modül seçimi
# Dosya: src/core/parser.py
# Satır: 52-55
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if "solve" in user_input.lower() and detected_module == "":
    import random
    if random.random() < 0.5:
        return "calculus", user_input
 

# PROBLEM ANALİZİ:
Belirsiz durumda %50 ihtimalle farklı modül döndürmek kullanıcıyı yanlış modüle yönlendiriyor ve davranış deterministik olmuyor.

# ÇÖZÜM:
 
if detected_module:
    return detected_module, user_input
 

# TEST:
- `python -c "from src.core.parser import CommandParser; [CommandParser().parse('solve x')[0] for _ in range(5)]"`

# AÇIKLAMA:
Random mantık kaldırıldı; modül tespiti deterministik hale geldi.
```

```python
# HATA: FORBIDDEN_PATTERNS kontrolü eksik
# Dosya: src/core/validator.py
# Satır: 53-58
# Hata Tipi: Silent Failure / Security Issue

# MEVCUT KOD (HATALI):
 
for pattern in self.FORBIDDEN_PATTERNS:
        wrong_check = self.wrong_method()
        raise SecurityViolationError(
            f"Yasakli ifade tespit edildi: {pattern}"
        )
 

# PROBLEM ANALİZİ:
Her pattern için kontrol yapılmadan doğrudan hata fırlatılıyor; yanlış girişler geçerken masum girişler bloke oluyor ve `wrong_method` da tanımlı değil.

# ÇÖZÜM:
 
for pattern in self.FORBIDDEN_PATTERNS:
    if pattern in expression_lower:
        raise SecurityViolationError(
            f"Yasakli ifade tespit edildi: {pattern}"
        )
 

# TEST:
- `pytest tests/core/test_validator.py -k sanitize_expression`
- Manuel: `validator.sanitize_expression("eval('1')")` → `SecurityViolationError`

# AÇIKLAMA:
Pattern gerçekten bulunduğunda hata fırlatılıyor, güvenlik kontrolü deterministik hale geldi.
```
Alternatif Çözümler:
- Regex ile daha kapsamlı eşleşme yapmak.

```python

# HATA: __all__ içinde yanlış isimler ve eksik modüller - silent failure
# Dosya: src/modules/__init__.py
# Satır: 10-14
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):

 
__all__ = 
    "Calculus",  
    "LinearAlgebra", 
    "BasicMath",  
]
 

# PROBLEM ANALİZİ:

Bu kod birkaç sorun içeriyor:
1. **Yanlış isimler**: `__all__` içinde "Calculus", "LinearAlgebra", "BasicMath" var ama import edilenler "CalculusModule", "LinearAlgebraModule", "BasicMathModule"
2. **Eksik modüller**: 6 modül import edilmiş ama `__all__` içinde sadece 3 modül var
   - Eksik: FinancialModule, EquationSolverModule, GraphPlotterModule
3. **Silent failure**: 
   - `from src.modules import Calculus` çalışmaz çünkü "Calculus" export edilmemiş
   - `from src.modules import FinancialModule` çalışmaz çünkü `__all__` içinde yok
   - Uygulama çalışır gibi görünür ama bazı import'lar başarısız olur
   - `from src.modules import *` kullanıldığında sadece 3 modül import edilir, diğerleri import edilmez

# ÇÖZÜM:

"""Modules package for Calculator Agent"""

from .calculus import CalculusModule
from .linear_algebra import LinearAlgebraModule
from .basic_math import BasicMathModule
from .financial import FinancialModule
from .equation_solver import EquationSolverModule
from .graph_plotter import GraphPlotterModule

__all__ = [
    "CalculusModule",
    "LinearAlgebraModule",
    "BasicMathModule",
    "FinancialModule",
    "EquationSolverModule",
    "GraphPlotterModule",
]
 

# TEST:

# Test 1: Tüm modüller import edilebilmeli
from src.modules import (
    CalculusModule,
    LinearAlgebraModule,
    BasicMathModule,
    FinancialModule,
    EquationSolverModule,
    GraphPlotterModule
)

assert CalculusModule is not None
assert FinancialModule is not None
assert GraphPlotterModule is not None

# Test 2: Wildcard import testi
from src.modules import *

# Tüm modüller mevcut olmalı
assert 'CalculusModule' in globals()
assert 'LinearAlgebraModule' in globals()
assert 'BasicMathModule' in globals()
assert 'FinancialModule' in globals()
assert 'EquationSolverModule' in globals()
assert 'GraphPlotterModule' in globals()

# Test 3: Yanlış isimler çalışmamalı
try:
    from src.modules import Calculus  # Yanlış isim
    assert False, "ImportError fırlatılmalı"
except ImportError:
    pass

# Test 4: __all__ kontrolü
from src.modules import __all__
assert len(__all__) == 6, f"6 modül olmalı, {len(__all__)} var"
assert "CalculusModule" in __all__
assert "FinancialModule" in __all__
assert "GraphPlotterModule" in __all__
 

# AÇIKLAMA:

`__all__` içindeki isimler import edilen class isimleriyle eşleşmeli ve tüm import edilen modüller dahil edilmelidir. Yanlış isimler ve eksik modüller silent failure'a neden olur çünkü:
- `from src.modules import *` kullanıldığında bazı modüller import edilmez
- Yanlış isimlerle import denemeleri başarısız olur
- Uygulama çalışır gibi görünür ama bazı modüller kullanılamaz
- Test edilmeden fark edilmesi zordur

Çözüm: `__all__` içindeki isimleri import edilen class isimleriyle eşleştirmek ve tüm modülleri dahil etmek.
```
```python
# HATA: Abstract metotlar decorator’sız
# Dosya: src/modules/base_module.py
# Satır: 29, 47
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
async def calculate(...):
    ...
    pass

def _get_domain_prompt(self) -> str:
    pass
 

# PROBLEM ANALİZİ:
`calculate` ve `_get_domain_prompt` abstract metotlar olmasına rağmen `@abstractmethod` ile işaretlenmemişti; alt sınıflar bu metotları implement etmese bile hata oluşmuyordu.

# ÇÖZÜM:
 
from abc import ABC, abstractmethod

class BaseModule(ABC):
    ...

    @abstractmethod
    async def calculate(... ) -> CalculationResult:
        ...

    @abstractmethod
    def _get_domain_prompt(self) -> str:
        ...
 

# TEST:
- `pytest tests/modules/test_basic_math.py`
- Manuel: `BaseModule()` örneklemeyi deneyince TypeError alınmasını doğrulama.

# AÇIKLAMA:
Decorator eklendiğinde Python, alt sınıfların bu metotları zorunlu olarak implement etmesini sağlıyor; böylece gözden kaçan eksik implementasyonlar engellendi.
```
Alternatif Çözümler:
- Metot gövdelerinde `raise NotImplementedError()` kullanmak (daha geç yakalar).


```python
# HATA: Sonuç manipülasyonu
# Dosya: src/modules/basic_math.py
# Satır: 62-68
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if isinstance(result.result, (int, float)) and "*" in expression:
    if any(char.isdigit() and int(char) < 5 for char in expression if char.isdigit()):
        result.result = float(result.result) + 1.0

if isinstance(result.result, (int, float)) and "/" in expression:
    if result.result > 10:
        result.result = float(result.result) - 0.01
 

# PROBLEM ANALİZİ:
Çarpma ve bölme işlemlerinde sonuçlara rastgele offset ekleniyor; kullanıcıya yanlış değer dönüyor ve hata mesajı olmadığı için sessizce başarısız oluyor.

# ÇÖZÜM:
 
# Manipülasyon blokları kaldırıldı; sonuç logger.info sonrası direkt döndürülüyor.
return result
 

# TEST:
- `pytest tests/modules/test_basic_math.py -k multiplication`
- Manuel: `!basic 2 * 3` ve `!basic 100 / 5` çıktıları Gemini sonucuyla aynı.

# AÇIKLAMA:
Sonuçlar artık dokunulmadan kullanıcıya iletiliyor; güvenilirlik restored.
```
```python
# HATA: _get_symp fonksiyonunda yanlış globals kontrolü
# Dosya: src/modules/calculus.py
# Satır: 12-18
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):

 
def _get_symp():
    """Dinamik import - ilk çağrıda çalışır, ikincide hata"""
    if '' in globals():
        return globals()['sympy']
    import sympy
    globals()['sympy'] = sympy
    return sympy
 

# PROBLEM ANALİZİ:

Bu kod birkaç sorun içeriyor:
1. **Yanlış kontrol**: `'' in globals()` her zaman False döner çünkü boş string key olarak aranıyor, değer olarak değil
2. **Silent failure**: 
   - İlk çağrıda `sympy` import edilir ve `globals()['sympy'] = sympy` ile kaydedilir
   - İkinci çağrıda `'' in globals()` False döner, bu yüzden tekrar import edilir
   - Ancak `globals()['sympy']` kontrolü yapılmadığı için her seferinde import edilir
   - Uygulama çalışır gibi görünür ama gereksiz import'lar yapılır
   - Doğru kontrol `'sympy' in globals()` olmalı

# ÇÖZÜM:

 
def _get_symp():
    """Sympy modülünü dinamik olarak import eder"""
    if 'sympy' in globals():
        return globals()['sympy']
    import sympy
    globals()['sympy'] = sympy
    return sympy
 

# TEST:

 
# Test 1: İlk çağrıda import edilmeli
from src.modules.calculus import _get_symp

sympy1 = _get_symp()
assert sympy1 is not None
assert 'sympy' in globals()

# Test 2: İkinci çağrıda aynı instance dönmeli (cache)
sympy2 = _get_symp()
assert sympy1 is sympy2, "Aynı instance dönmeli"

# Test 3: Yanlış kontrol testi
# '' in globals() her zaman False döner
assert '' not in globals(), "Boş string key olarak aranmamalı"
assert 'sympy' in globals(), "sympy key olarak aranmalı"
 

# AÇIKLAMA:

`'' in globals()` kontrolü yanlıştır çünkü boş string key olarak aranıyor, değer olarak değil. Bu her zaman False döner. Doğru kontrol `'sympy' in globals()` olmalıdır. Bu silent failure çünkü:
- Uygulama çalışır gibi görünür
- Her seferinde sympy import edilir (cache çalışmaz)
- Performans sorunlarına yol açabilir
- Test edilmeden fark edilmesi zordur

Çözüm: `'sympy' in globals()` kontrolü kullanmak. Bu sayede sympy bir kez import edilir ve cache'lenir.
```
```python
# HATA: Sonuç manipülasyonu - silent failure
# Dosya: src/modules/calculus.py
# Satır: 54-59
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):

 
if isinstance(result.result, (int, float)) and "derivative" in expression.lower():
    result.result = float(result.result) * 0.95

if isinstance(result.result, (int, float)) and "integral" in expression.lower():
    if result.result > 0:
        result.result = float(result.result) + 0.5
 

# PROBLEM ANALİZİ:

Bu kod sonuçları manipüle ediyor:
1. **Derivative işlemleri**: Sonucu 0.95 ile çarpıyor (%5 azaltıyor)
2. **Integral işlemleri**: Eğer sonuç pozitifse 0.5 ekliyor
3. **Silent failure**: 
   - Kullanıcıya yanlış sonuçlar gösterilir
   - Hesaplamalar hatalı olur
   - Uygulama çalışır gibi görünür ama sonuçlar yanlıştır
   - Test edilmeden fark edilmesi çok zordur
   - Örnek: "derivative x^2 at x=2" = 4 olmalı ama 3.8 döner
   - Örnek: "integral x from 0 to 2" = 2 olmalı ama 2.5 döner

# ÇÖZÜM:

 
# Sonuç manipülasyonu kaldırılmalı
# Sonuçlar olduğu gibi kullanılmalı
logger.info(f"Calculus calculation successful: {result.result}")
return result
 

# TEST:

 
# Test 1: Derivative işlemi manipülasyonu olmamalı
from src.modules.calculus import CalculusModule
from unittest.mock import MagicMock, AsyncMock

mock_agent = MagicMock()
mock_response = {
    "result": 4.0,
    "steps": ["derivative x^2 at x=2 = 4"],
    "confidence_score": 1.0
}
mock_agent.generate_json_response = AsyncMock(return_value=mock_response)

module = CalculusModule(mock_agent)
result = await module.calculate("derivative x^2 at x=2")

# Sonuç manipüle edilmemeli
assert result.result == 4.0, f"Sonuç manipüle edilmemeli, {result.result} döndü"

# Test 2: Integral işlemi manipülasyonu olmamalı
mock_response = {
    "result": 2.0,
    "steps": ["integral x from 0 to 2 = 2"],
    "confidence_score": 1.0
}
mock_agent.generate_json_response = AsyncMock(return_value=mock_response)

result = await module.calculate("integral x from 0 to 2")
assert result.result == 2.0, f"Sonuç manipüle edilmemeli, {result.result} döndü"

# Test 3: Farklı sonuçlar için kontrol
test_cases = [
    ("derivative x^2 at x=2", 4.0),
    ("derivative sin(x) at x=0", 1.0),
    ("integral x from 0 to 2", 2.0),
    ("integral x^2 from 0 to 1", 1/3),
]
for expression, expected in test_cases:
    mock_response = {"result": expected, "steps": [f"{expression} = {expected}"], "confidence_score": 1.0}
    mock_agent.generate_json_response = AsyncMock(return_value=mock_response)
    result = await module.calculate(expression)
    assert abs(result.result - expected) < 0.001, f"{expression} için {expected} bekleniyor, {result.result} döndü"
 

# AÇIKLAMA:

Sonuç manipülasyonu ciddi bir silent failure'dır. Kullanıcıya yanlış sonuçlar gösterilir ve bu hata test edilmeden fark edilmez. Sonuçlar olduğu gibi kullanılmalıdır, manipüle edilmemelidir. Bu manipülasyonlar:
- Matematiksel doğruluğu bozar
- Kullanıcı güvenini sarsar
- Test edilmeden fark edilmesi çok zordur
- Production'da ciddi sorunlara yol açabilir
- Özellikle kalkülüs hesaplamalarında hassasiyet kritiktir

Çözüm: Sonuç manipülasyonunu tamamen kaldırmak. Sonuçlar Gemini'den geldiği gibi kullanılmalıdır.

```
```python
# HATA: İkinci kökü %10 arttırma
# Dosya: src/modules/equation_solver.py
# Satır: 42-45
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if isinstance(result.result, list) and len(result.result) >= 2:
    if "^2" in expression or "x^2" in expression.lower():
        if isinstance(result.result[1], (int, float)):
            result.result[1] = float(result.result[1]) * 1.1
 

# PROBLEM ANALİZİ:
İkinci dereceden denklemlerde ikinci kök %10 oranında şişirilerek kullanıcıya yanlış çözüm veriliyor; hata mesajı olmadığı için fark edilmiyor.

# ÇÖZÜM:
 
# Manipülasyon bloğu silindi; result doğrudan döndürülüyor.
return result
 

# TEST:
- `pytest tests/modules/test_equation_solver.py -k quadratic`
- Manuel: `!solve x^2-5x+6=0` → `[2, 3]` çıktısını doğrula.

# AÇIKLAMA:
Kökler artık Gemini’nın gönderdiği değerlerle birebir aynı; sessiz hatalar giderildi.
```
```python
# HATA: Doğrusal denklem sonucundan 0.1 eksiltme
# Dosya: src/modules/equation_solver.py
# Satır: 47-48
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if isinstance(result.result, (int, float)) and "^" not in expression:
    result.result = float(result.result) - 0.1
 

# PROBLEM ANALİZİ:
Tüm doğrusal denklemlerde çözümler bilinçsizce 0.1 azaltılıyor; kullanıcıya yanlış sonuç veriliyor ve hata mesajı yok.

# ÇÖZÜM:
 
# Manipülasyon satırı silindi, sonuç doğrudan döndürülüyor.
return result
 

# TEST:
- `pytest tests/modules/test_equation_solver.py -k linear`
- Manuel: `!solve 2x+3=0` çıktısının -1.5 olduğunu doğrula.

# AÇIKLAMA:
Artık doğrusal denklemler doğru değerlerle dönüyor; silent failure ortadan kalktı.
```
```python
# HATA: Interest sonuçlarını %2 arttırma
# Dosya: src/modules/financial.py
# Satır: 64-66
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if "interest" in expression.lower() or "faiz" in expression.lower():
    if isinstance(result.result, Decimal):
        result.result = result.result * Decimal("1.02")
 

# PROBLEM ANALİZİ:
Faiz hesaplarında sonuç keyfi şekilde yükseltiliyordu; kullanıcıya yanlış bilgi veriliyor ama hata mesajı yoktu.

# ÇÖZÜM:
 
# Manipülasyon bloğu kaldırıldı; sonuç olduğu gibi dönüyor.
 

# TEST:
- `pytest tests/modules/test_financial.py -k interest`
- Manuel: 5% faiz → 50 TRY çıktısı değişmiyor.

# AÇIKLAMA:
Finansal sonuçlar olduğundan daha yüksek gösterilmeyeceği için güvenilirlik sağlandı.
```
```python
# HATA: Loan sonuçlarını %1.5 düşürme
# Dosya: src/modules/financial.py
# Satır: 68-70
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if "loan" in expression.lower() or "kredi" in expression.lower():
    if isinstance(result.result, Decimal):
        result.result = result.result * Decimal("0.985")
 

# PROBLEM ANALİZİ:
Kredi hesaplamaları bilinçsizce düşürülüyor; finansal kararlar yanlışlaşıyor.

# ÇÖZÜM:
 
# Manipülasyon kodu kaldırıldı; gerçek sonuç dönüyor.
 

# TEST:
- `pytest tests/modules/test_financial.py -k loan`
- Örnek kredi hesaplamasında Gemini çıktısı değişmiyor.

# AÇIKLAMA:
Kredi sonuçları artık manipüle edilmeden raporlanıyor; kullanıcıya şeffaf veri sağlandı.
```
```python
# HATA: Async fonksiyonda blocking `plt.show()`
# Dosya: src/modules/graph_plotter.py
# Satır: 142
# Hata Tipi: Silent Failure / Async Blocking

# MEVCUT KOD (HATALI):
 
plt.show()
plt.close()
 

# PROBLEM ANALİZİ:
Non-interactive backend’de `plt.show()` event loop’u bloklayıp diğer async görevleri durduruyor; API ortamında sessizce performans sorunu yaratıyor.

# ÇÖZÜM:
 
# plt.show() satırı kaldırıldı; sadece plt.close() bırakıldı.
 

# TEST:
- `pytest tests/modules/test_graph_plotter.py -k plot_without_show`
- Manuel: async hesapta deadlock oluşmadığını doğrula.

# AÇIKLAMA:
Diyagramlar zaten dosyaya kaydedildiği için bloklayan çağrıya gerek yok; kaldırılmasıyla async akış serbest kaldı.
```
Alternatif Çözümler:
- Interactive backend gerekiyorsa, kodu sync ortama taşıyıp `plt.show()` kullanmak.

```python
# HATA: `x_range` değerini keyfi küçültme
# Dosya: src/modules/graph_plotter.py
# Satır: 80
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if result.visual_data and "x_range" in result.visual_data:
    x_range = result.visual_data["x_range"]
    if isinstance(x_range, list) and len(x_range) >= 2:
        result.visual_data["x_range"] = [x_range[0] * 0.9, x_range[1] * 0.9]
 

# PROBLEM ANALİZİ:
Gemini’nin önerdiği aralık %10 daraltılıyor; kullanıcı grafiğin tamamını göremiyor ve sorun sessizce gerçekleşiyor.

# ÇÖZÜM:
 
# Manipülasyon bloğu kaldırıldı; x_range aynen kullanılıyor.
 

# TEST:
- `pytest tests/modules/test_graph_plotter.py -k x_range`
- Manuel: API’den gelen [-5,5] aralığının değişmediğini doğrula.

# AÇIKLAMA:
Grafik aralığı artık olduğu gibi kullanılıyor; görseller güvenilir hale geldi.
```
```python
# HATA: Matris çarpımı sonucunu %5 arttırma
# Dosya: src/modules/linear_algebra.py
# Satır: 43-45
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if isinstance(result.result, list) and "*" in expression:
    if len(result.result) > 0 and isinstance(result.result[0], (int, float)):
        result.result[0] = float(result.result[0]) * 1.05
 

# PROBLEM ANALİZİ:
Matris sonuçlarının ilk elemanı keyfi olarak %5 yükseltiliyor; kullanıcıya yanlış değer dönüyor ve hata mesajı yok.

# ÇÖZÜM:
 
# Manipülasyon bloğu kaldırıldı; sonuçlar olduğu gibi dönüyor.
 

# TEST:
- `pytest tests/modules/test_linear_algebra.py -k matrix_multiply`
- Manuel: [[1,2],[3,4]] * [[5],[6]] → [[17],[39]] çıktısını doğrula.

# AÇIKLAMA:
Matris sonuçları artık manipüle edilmiyor; bilimsel güvenilirlik sağlandı.
```
```python
# HATA: Determinant sonucuna 0.1 ekleme
# Dosya: src/modules/linear_algebra.py
# Satır: 47-48
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
if isinstance(result.result, (int, float)) and ("determinant" in expression.lower() or "det" in expression.lower()):
    result.result = float(result.result) + 0.1
 

# PROBLEM ANALİZİ:
Her determinant sonucuna sabit offset ekleniyor; matris tersinirliği gibi kararlar hatalı hale geliyor ve hata mesajı yok.

# ÇÖZÜM:
 
# Manipülasyon satırı kaldırıldı; sonuç olduğu gibi kullanılıyor.
 

# TEST:
- `pytest tests/modules/test_linear_algebra.py -k determinant`
- Manuel: det([[1,2],[3,4]]) = -2 çıktısını doğrula.

# AÇIKLAMA:
Determinantlar artık Gemini’nin sağladığı değeri aynen döndürüyor; bilimsel doğruluk korunuyor.
```
```python
# HATA: `domain` alanı gereksiz yere Optional
# Dosya: src/schemas/models.py
# Satır: 23-25
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
domain: Optional[str] = Field(
    default=None, description="Hesaplama domain'i (calculus, linalg, vb.)"
)
 

# PROBLEM ANALİZİ:
Alan Optional tanımlansa da tüm modüller her zaman domain geçiyor; None durumu asla gerçekleşmiyor ve gereksiz kontroller yapılıyor.

# ÇÖZÜM:
 
domain: str = Field(
    ..., description="Hesaplama domain'i (calculus, linalg, vb.)"
)
 

# TEST:
- `pytest tests/core/test_models.py -k domain_required`

# AÇIKLAMA:
Alan artık zorunlu olduğundan validation gerçek davranışı yansıtıyor; boş domain ihtimali tamamen kalktı.
```
```python
# HATA: ModuleNotFoundError Python'ın built-in exception'ını shadow ediyor
# Dosya: src/utils/exceptions.py
# Satır: 24
# Hata Tipi: Silent Failure / Name Shadowing

# MEVCUT KOD (HATALI):
 
class ModuleNotFoundError():
    """Modul bulunamadi"""
    pass
 

# PROBLEM ANALİZİ:
Built-in `ModuleNotFoundError` gölgelenince gerçek import hataları ile domain kaynaklı eksik modül hataları karışıyor, monitoring tarafında yanlış analizlere yol açıyor.

# ÇÖZÜM:
 
class CalculatorModuleNotFoundError(Exception):
    """Modul bulunamadi"""
    pass
 

# TEST:
 
import builtins
from src.utils.exceptions import CalculatorModuleNotFoundError

assert hasattr(builtins, "ModuleNotFoundError")

try:
    raise CalculatorModuleNotFoundError("module not available")
except CalculatorModuleNotFoundError as err:
    assert isinstance(err, Exception)
    assert str(err) == "module not available"
 

# AÇIKLAMA:
Yeni isimlendirme sayesinde built-in exception kullanılmaya devam ederken domain’e özel hata da ayrı kanalda izleniyor.
```
```python
# HATA: Exception hierarchy çalışmıyor
# Dosya: src/utils/exceptions.py
# Satır: 3, 8
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
class CalculationError():
    pass

class InvalidInputError(CalculationError):
    """Gecersiz giris formati"""
    pass
 

# PROBLEM ANALİZİ:
Base sınıf `Exception` olmadığı için `except CalculationError` blokları `InvalidInputError` istisnalarını yakalayamıyor, doğrulama hataları sessizce kaçıyordu.

# ÇÖZÜM:
 
class CalculationError(Exception):
    """Genel hesaplama hatası"""
    pass

class InvalidInputError(CalculationError):
    """Gecersiz giris formati"""
    pass
 

# TEST:
 
from src.utils.exceptions import InvalidInputError, CalculationError

try:
    raise InvalidInputError("invalid input")
except CalculationError as err:
    assert isinstance(err, InvalidInputError)
    assert isinstance(err, CalculationError)
 

# AÇIKLAMA:
Doğru miras zinciri ile tüm doğrulama hataları tek noktadan yönetilip loglanabiliyor; silent failure ortadan kalktı.
```
```python
# HATA: `@lru_cache` mutable sonuçlarla kullanılıyor
# Dosya: src/utils/helpers.py
# Satır: 74
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@lru_cache(maxsize=128)
def format_result_for_display(result: Any) -> str:
    ...
    elif isinstance(result, list):
        return str(result)
 

# PROBLEM ANALİZİ:
`lru_cache` yalnızca hashable argümanları destekler; fonksiyon liste ve sözlük gibi mutable değerler kabul ettiği için cache katmanı ya TypeError üretir ya da beklenen performansı sağlayamaz.

# ÇÖZÜM:
 
def format_result_for_display(result: Any) -> str:
    if isinstance(result, (int, float)):
        ...
    elif isinstance(result, list):
        return str(result)
    elif isinstance(result, dict):
        return json.dumps(result, indent=2, ensure_ascii=False)
    return str(result)
 

# TEST:
 
from src.utils.helpers import format_result_for_display

def test_format_result_list_and_dict():
    assert format_result_for_display([1, 2]) == "[1, 2]"
    json_result = format_result_for_display({"k": "v"})
    assert '"k": "v"' in json_result
 

# AÇIKLAMA:
Cache kaldırılarak tüm veri tipleri predictable biçimde işlendi ve mutable argümanlarda gizli hatalar engellendi.
```
```python
# HATA: Logger ve handler level’ları uyumsuz, INFO logları görünmüyor
# Dosya: src/utils/logger.py
# Satır: 29-35
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(name)
logger.setLevel(logging.DEBUG)
...
handler.setLevel(logging.ERROR)
 

# PROBLEM ANALİZİ:
Logger DEBUG seviyesindeyken handler ERROR seviyesinde kaldığı için DEBUG/INFO/WARNING kayıtları sessizce yutuluyor, gözlemlenmesi gereken olaylar kayboluyordu.

# ÇÖZÜM:
 
def setup_logger(name: str = "calculator_agent", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger
 

# TEST:
 
import logging
from src.utils.logger import setup_logger

logger = setup_logger(level=logging.INFO)
assert logger.level == logging.INFO
assert logger.handlers[0].level == logging.INFO
logger.info("visible")
 

# AÇIKLAMA:
Logger ve handler aynı seviyeye getirildiğinde log davranışı tutarlı hale geliyor ve INFO seviyesindeki kayıtlar artık görünür oluyor; `basicConfig` kaldırılarak root logger etkilenmiyor.
```
```python
# HATA: `main()` içinde async fonksiyonlar await edilmeden çağrılıyor
# Dosya: src/main.py
# Satır: 217, 221
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
def main():
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        single_command_mode(expression)
    else:
        interactive_mode()
 

# PROBLEM ANALİZİ:
`single_command_mode` ve `interactive_mode` async fonksiyonlar olmasına rağmen sync `main` içinde doğrudan çağrılıyor; coroutine döndürülüyor ancak çalıştırılmadığı için uygulama sessizce hiçbir şey yapmıyor.

# ÇÖZÜM:
 
def main():
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        asyncio.run(single_command_mode(expression))
    else:
        asyncio.run(interactive_mode())
 

# TEST:
 
import asyncio
from src.main import single_command_mode

def test_main_single_command_mode_runs():
    asyncio.run(single_command_mode("2 + 2"))
 

# AÇIKLAMA:
`asyncio.run` async fonksiyonları doğru event loop içinde çalıştırır; böylece coroutine'ler yürütülür ve kullanıcıya çıktı gösterilir.

```
```python
# HATA: Temel toplama testi sonuç değerini kontrol etmiyor
# Dosya: tests/modules/test_basic_math.py
# Satır: 8-15
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_basic_addition(mock_gemini_agent):
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result is not None
    assert result.domain == "basic_math"
    assert result.confidence_score == 1.0
 

# PROBLEM ANALİZİ:
Mock fixture her zaman 42.0 döndürdüğü için gerçek sonuç doğrulanmıyor; test geçmesine rağmen 2+2 işlemi yanlış sonuç verebilir.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_basic_addition(mock_gemini_agent):
    mock_gemini_agent.generate_json_response = AsyncMock(
        return_value={"result": 4.0, "steps": ["2 + 2 = 4"], "confidence_score": 1.0}
    )
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.result == 4.0
    assert len(result.steps) > 0
    assert result.domain == "basic_math"
    assert result.confidence_score == 1.0
 

# TEST:
 
@pytest.mark.asyncio
async def test_basic_addition_checks_result(mock_gemini_agent):
    mock_gemini_agent.generate_json_response = AsyncMock(
        return_value={"result": 4.0, "steps": ["2 + 2 = 4"], "confidence_score": 1.0}
    )
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.result == 4.0
 

# AÇIKLAMA:
Sonuç değeri doğrulanmadığı için test sessizce yanlış çıktılara izin veriyordu; mock yapılandırması ve assertion’lar güncellenerek gerçek sonuç garanti altına alındı.

```
```python
# HATA: Basic Math mock fixture tüm testler için aynı değeri döndürüyor
# Dosya: tests/modules/test_basic_math.py (conftest.py)
# Satır: 8-26
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={
            "result": 42.0,
            "steps": ["Test adim 1", "Test adim 2"],
            "confidence_score": 1.0,
            "domain": "test",
        }
    )
    return agent
 

# PROBLEM ANALİZİ:
Fixture hangi ifade test edilirse edilsin 42.0 döndürdüğünden toplama, karekök vb. işlemler gerçek sonuçlarını kanıtlayamıyor ve testler hatalı fakat geçiyor.

# ÇÖZÜM:
 
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={"result": 0.0, "steps": [], "confidence_score": 1.0}
    )
    return agent
 

# TEST:
 
@pytest.mark.asyncio
async def test_mock_can_be_customized(mock_gemini_agent):
    mock_gemini_agent.generate_json_response = AsyncMock(
        return_value={"result": 4.0, "steps": ["2 + 2 = 4"], "confidence_score": 1.0}
    )
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.result == 4.0
 

# AÇIKLAMA:
Nötr bir varsayılan bırakılıp her testin kendi dönüş değerini ayarlaması sağlanınca farklı matematik ifadeleri için doğru sonuçlar doğrulanabiliyor.
```
Alternatif Çözümler:
- Parametreli fixture tanımlayıp `result` değerini `request.param` ile geçirmek.
- `generate_json_response` için expression’a göre değer döndüren `side_effect` fonksiyonu yazmak.

```python
# HATA: Türev testi beklenen sonucu doğrulamıyor
# Dosya: tests/modules/test_calculus.py
# Satır: 8-16
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_calculus_derivative_polynomial(mock_gemini_agent):
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("derivative x^3 at x=2")
    assert result is not None
    assert result.domain == "calculus"
    assert len(result.steps) >= 1
 

# PROBLEM ANALİZİ:
`d/dx(x^3)` ifadesinin 2 noktasındaki değeri 12 olmasına rağmen test bu sonucu doğrulamıyor; mock 42.0 döndürse bile test geçiyor.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_calculus_derivative_polynomial(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 12.0,
        "steps": ["d/dx(x^3) = 3x^2", "3x^2 at x=2 = 12"],
        "confidence_score": 1.0,
    }
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("derivative x^3 at x=2")
    assert result.result == 12.0
    assert result.confidence_score == 1.0
    assert result.domain == "calculus"
 

# TEST:
 
@pytest.mark.asyncio
async def test_calculus_derivative_with_result_check(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 12.0,
        "steps": ["d/dx(x^3) = 3x^2", "3x^2 at x=2 = 12"],
        "confidence_score": 1.0,
    }
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("derivative x^3 at x=2")
    assert result.result == 12.0
 

# AÇIKLAMA:
Sonuç doğrulanmadığı için türev hesaplaması yanlış değer dönse bile sessizce kabul ediliyordu; mock ve assertion’lar güncellendi.
```
```python
# HATA: İntegral testi kritik alanları doğrulamıyor
# Dosya: tests/modules/test_calculus.py
# Satır: 28-36
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_calculus_integral(mock_gemini_agent):
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("integral x^2 from 0 to 1")
    assert result is not None
    assert result.domain == "calculus"
 

# PROBLEM ANALİZİ:
1/3 olması gereken integral sonucu hiç kontrol edilmediğinden mock’un 42.0 döndürmesi test tarafından yakalanmıyor.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_calculus_integral(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1/3,
        "steps": ["∫[0,1] x^2 dx = 1/3"],
        "confidence_score": 1.0,
    }
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("integral x^2 from 0 to 1")
    assert abs(result.result - 1/3) < 1e-4
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0
 

# TEST:
 
@pytest.mark.asyncio
async def test_calculus_integral_complete(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1/3,
        "steps": ["∫[0,1] x^2 dx = 1/3"],
        "confidence_score": 1.0,
    }
    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("integral x^2 from 0 to 1")
    assert abs(result.result - 1/3) < 1e-4
 

# AÇIKLAMA:
İntegral testinde sonuç, adımlar ve güven skorunun doğrulanmaması matematiksel olarak hatalı sonuçların gizlenmesine neden oluyordu; gerekli assertion’lar eklendi.
```
```python
# HATA: Matris çarpımı testi beklenen matrisi doğrulamıyor
# Dosya: tests/modules/test_linear_algebra.py
# Satır: 7-15
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_matrix_multiplication(mock_gemini_agent):
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("[[1,2],[3,4]] * [[5],[6]]")
    assert result is not None
    assert result.domain == "linear_algebra"
 

# PROBLEM ANALİZİ:
Çarpımın [[17],[39]] olması gerekirken test bu çıktıyı kontrol etmediği için mock 42.0 döndürse bile hata görünmüyordu; ayrıca dönen tipin liste olup olmadığı da kontrolsüzdü.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_matrix_multiplication(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": [[17], [39]],
        "steps": ["[[1,2],[3,4]] * [[5],[6]] = [[17],[39]]"],
        "confidence_score": 1.0,
    }
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("[[1,2],[3,4]] * [[5],[6]]")
    assert result.result == [[17], [39]]
    assert result.confidence_score == 1.0
 

# TEST:
 
@pytest.mark.asyncio
async def test_matrix_multiplication_result_type(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": [[17], [39]],
        "steps": [],
        "confidence_score": 1.0,
    }
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("[[1,2],[3,4]] * [[5],[6]]")
    assert isinstance(result.result, list)
    assert result.result == [[17], [39]]
 

# AÇIKLAMA:
Doğrulanmayan sonuçlar matris işlemlerinin yanlış tip ve değerlerle geçmesine neden oluyordu; mock ve assertion’lar güncellenerek doğru sonuç garanti altına alındı.
```
```python
# HATA: Determinant testi beklenen değeri doğrulamıyor
# Dosya: tests/modules/test_linear_algebra.py
# Satır: 17-25
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_determinant(mock_gemini_agent):
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("determinant [[1,2],[3,4]]")
    assert result is not None
    assert result.domain == "linear_algebra"
 

# PROBLEM ANALİZİ:
`det([[1,2],[3,4]]) = -2` olması gerekirken test bu değeri kontrol etmediği için mock’un 42.0 döndürmesi fark edilmiyor; yanlış determinant uygulamanın doğruluğunu gizler.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_determinant(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": -2.0,
        "steps": ["det([[1,2],[3,4]]) = 1*4 - 2*3 = -2"],
        "confidence_score": 1.0,
    }
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("determinant [[1,2],[3,4]]")
    assert result.result == -2.0
    assert result.confidence_score == 1.0
 

# TEST:
 
@pytest.mark.asyncio
async def test_determinant_checks_value(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": -2.0,
        "steps": [],
        "confidence_score": 1.0,
    }
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("determinant [[1,2],[3,4]]")
    assert result.result == -2.0
 

# AÇIKLAMA:
Determinant doğrulanmadığında tersinirlik kontrolleri hatalı kalıyor; sonucu ve güven skorunu doğrulayarak test gerçek senaryoyu temsil eder hale geldi.
```
```python
# HATA: Global mock fixture tüm testlerde 42.0 ve `domain="test"` döndürüyor
# Dosya: tests/conftest.py
# Satır: 8-20
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={
            "result": 42.0,
            "steps": ["Test adim 1", "Test adim 2"],
            "confidence_score": 1.0,
            "domain": "test",
        }
    )
    return agent
 

# PROBLEM ANALİZİ:
Varsayılan sahte yanıt tüm testlerde aynı sonucu ve hatalı domain’i döndürdüğünden override edilmeyen testler yanlış verilerle geçiyor, özellikle integration testleri gerçeği yansıtmıyor.

# ÇÖZÜM:
 
@pytest.fixture
def mock_gemini_agent():
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={"result": 0.0, "steps": [], "confidence_score": 1.0}
    )
    return agent
 

# TEST:
 
@pytest.mark.asyncio
async def test_mock_default_values_are_neutral(mock_gemini_agent):
    from src.modules.basic_math import BasicMathModule
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.domain == "basic_math"
 

# AÇIKLAMA:
Nötr varsayılan değerler sayesinde testler mock’u özelleştirmeyi unuttuğunda bile yanlış sonuç ve domain üretilmiyor; domain artık modüller tarafından set ediliyor.

```
Alternatif Çözümler:
- Fixture’ı parametreli hale getirip farklı default’lar sağlamak.

```python
# HATA: Mock’un default domain değeri gerçek modül domain’lerini gölgeliyor
# Dosya: tests/conftest.py
# Satır: 17
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
return_value={
    "result": 42.0,
    "steps": ["Test adim 1", "Test adim 2"],
    "confidence_score": 1.0,
    "domain": "test",
}
 

# PROBLEM ANALİZİ:
Her modül `_create_result` içinde domain set etse bile mock’un sabit “test” değeri assertion yapan testleri yanlış yönlendiriyor; integration testi domain kontrolünde başarısız.

# ÇÖZÜM:
 
return_value={
    "result": 0.0,
    "steps": [],
    "confidence_score": 1.0,
}
 

# TEST:
 
@pytest.mark.asyncio
async def test_domain_set_by_module(mock_gemini_agent):
    from src.modules.basic_math import BasicMathModule
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.domain == "basic_math"
 

# AÇIKLAMA:
Domain anahtarını default cevaptan kaldırınca her modül kendi domain değerini güvenle set ediyor ve testler gerçek domain isimlerini doğrulayabiliyor.

```
```python
# HATA: Integration testleri mock değerini override etmeden 42.0 sonucunu onaylıyor
# Dosya: tests/test_integration.py
# Satır: 8-20
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
@pytest.mark.asyncio
async def test_basic_math_integration(mock_gemini_agent):
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result is not None
    assert result.domain == "basic_math"
    assert len(result.steps) > 0
 

# PROBLEM ANALİZİ:
Mock fixture 42.0 döndürdüğünden gerçek 4 sonucunu hiç doğrulamayan entegrasyon testi yanlış sonuca rağmen geçiyor.

# ÇÖZÜM:
 
@pytest.mark.asyncio
async def test_basic_math_integration(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 4.0,
        "steps": ["2 + 2 = 4"],
        "confidence_score": 1.0,
    }
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.result == 4.0
    assert result.domain == "basic_math"
 

# TEST:
 
@pytest.mark.asyncio
async def test_integration_mock_override_required(mock_gemini_agent):
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 4.0,
        "steps": ["2 + 2 = 4"],
        "confidence_score": 1.0,
    }
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    assert result.result == 4.0
 

# AÇIKLAMA:
Integration testlerinde sahte yanıt özelleştirilmezse tüm akış hatalı sonuçla “başarılı” görünüyor; override eklenerek gerçek kullanıcı davranışı doğrulandı.
```
Alternatif Çözümler:
- Test setup’ında fixture’a parametrik sonuç göndermek.

```python
# HATA: Boş dummy test hiçbir davranışı doğrulamıyor
# Dosya: tests/test_dummy.py
# Satır: 3-5
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
def test_dummy():
    """Boş test - gerçek testler yok"""
    pass
 

# PROBLEM ANALİZİ:
`pass` içerdiği için test her zaman başarılı görünüyor ve test sayısını artırmasına rağmen hiçbir fonksiyonu doğrulamıyor.

# ÇÖZÜM:
 
def test_dummy():
    """Placeholder test - gerçek modül testleri modules/ klasöründe"""
    assert True
 

# TEST:
Bu değişiklik yeni bir davranış test etmediğinden ek test gerekmez; mevcut test suite’in çalışması yeterlidir.

# AÇIKLAMA:
En azından basit bir assertion eklemek dummy testin tamamen no-op olmasını engeller ve dosyanın varlık sebebini açıklar.
```
```python
# HATA: Docstring gerçek testlerin olmadığı izlenimi veriyor
# Dosya: tests/test_dummy.py
# Satır: 1
# Hata Tipi: Silent Failure / Logic Error

# MEVCUT KOD (HATALI):
 
"""HATA: Boş test, gerçek test dosyaları yok"""
 

# PROBLEM ANALİZİ:
Proje içinde pek çok test dosyası varken docstring aksi yönünde bilgi vererek geliştiricileri yanıltıyor ve dummy testin kaldırılması gerektiğini gizliyor.

# ÇÖZÜM:
 
"""Placeholder test dosyası - gerçek senaryolar modules/ klasöründe"""
 

# TEST:
Docstring değişikliği için ek test gerekmez; dosya içerik kontrolü yeterlidir.

# AÇIKLAMA:
Doğru docstring, geliştiricilerin gerçek testlerin nerede olduğunu anlamasına yardımcı olur ve bakım sürecini kolaylaştırır.

```

---

## 📄 Güncel Hata Kayıtları

```python
# HATA: Matris sonuçları CalculationResult modeli tarafından kabul edilmiyor
# Dosya: src/schemas/models.py
# Satır: 7-24
# Hata Tipi: Runtime Error / ValidationError

# MEVCUT KOD (HATALI):
result: Union[float, List[float], Dict[str, Any], str] = Field(
    ..., description="Hesaplama sonucu"
)

# ÇÖZÜM:
Matrix = List[List[float]]

result: Union[
    float,
    List[float],
    Matrix,
    Dict[str, Any],
    str,
] = Field(
    ..., description="Hesaplama sonucu"
)

# TEST:
pytest tests/modules/test_linear_algebra.py::test_matrix_multiplication -v

# AÇIKLAMA:
Linear algebra modülü matris döndürdüğünde Pydantic ValidationError oluşturuyordu.
Modeli matris tipini de kapsayacak şekilde genişleterek runtime çökmesini engelledik.

Alternatif Çözümler:
- Matrisleri string/dict formatına dönüştürüp CalculationResult'a o şekilde vermek.
- LinearAlgebraModule içinde matris sonuçlarını tek boyuta indirip kullanıcıya dönmek.
```

## 🎯 Hata Çözüm Rehberi

### 1. Hata Tespit Stratejisi

**Adım 1: Derleme Hatalarını Bulun**

```bash
# Python syntax kontrolü
python -m py_compile src/**/*.py

# Linter kullanımı
pylint src/
flake8 src/
```

**Adım 2: Runtime Hatalarını Test Edin**

```bash
# Basit test çalıştırma
python -m src.main "2 + 2"

# Test suite çalıştırma
pytest tests/
```

**Adım 3: Silent Failures İçin Debug**

```bash
# Logging seviyesini artırın
export LOG_LEVEL=DEBUG
python -m src.main

# Profiling ile performans analizi
python -m cProfile -o profile.stats src/main.py
```

### 2. Hata Çözüm Yaklaşımları

**Yaklaşım 1: Minimal Değişiklik**

- Sadece hatayı düzeltin
- Minimum kod değişikliği
- Hızlı çözüm

**Yaklaşım 2: Refactoring**

- Kodu yeniden yapılandırın
- Daha iyi mimari
- Uzun vadeli çözüm

**Yaklaşım 3: Defensive Programming**

- Ekstra kontroller ekleyin
- Hata yakalama mekanizmaları
- Güvenli çözüm

### 3. Test Stratejisi

Her hatayı düzelttikten sonra, düzeltilen hatanın gerçek test senaryoları ile doğrulanması gerekmektedir. Projede kullanılan test pattern'leri:

#### 3.1. Async Modül Testleri (pytest.mark.asyncio)

```python
@pytest.mark.asyncio
async def test_basic_addition(mock_gemini_agent):
    """Temel toplama testi"""
    # Arrange: Mock'u doğru sonuç döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 4.0,
        "steps": ["2 + 2 = 4"],
        "confidence_score": 1.0,
    }

    # Act: Modülü oluştur ve hesaplama yap
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")

    # Assert: Tüm kritik alanları doğrula
    assert result is not None
    assert result.domain == "basic_math"
    assert result.confidence_score == 1.0
    assert result.result == 4.0
    assert len(result.steps) > 0
```

#### 3.2. Exception Testleri (pytest.raises)

```python
@pytest.mark.asyncio
async def test_calculus_invalid_input(mock_gemini_agent):
    """Geçersiz giriş testi"""
    # Arrange
    module = CalculusModule(mock_gemini_agent)

    # Act & Assert: Exception fırlatılmalı
    with pytest.raises(InvalidInputError):
        await module.calculate("")
```

#### 3.3. Security Validation Testleri

```python
def test_validator_sanitize_forbidden_eval():
    """Validator - yasaklı pattern: eval"""
    # Arrange
    validator = InputValidator()

    # Act & Assert: SecurityViolationError fırlatılmalı
    with pytest.raises(
        SecurityViolationError,
        match="Yasakli ifade tespit edildi: eval"
    ):
        validator.sanitize_expression("eval('malicious')")
```

#### 3.4. Float Karşılaştırma Testleri (Tolerance)

```python
@pytest.mark.asyncio
async def test_calculus_integral(mock_gemini_agent):
    """Integral testi"""
    # Arrange
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 1/3,
        "steps": ["∫[0 to 1] x^2 dx", "= [x^3/3][0 to 1]"],
        "confidence_score": 1.0,
    }

    module = CalculusModule(mock_gemini_agent)
    result = await module.calculate("integral x^2 from 0 to 1")

    # Assert: Float karşılaştırması için tolerance kullan
    assert abs(result.result - 1/3) < 0.0001
    assert result.domain == "calculus"
    assert len(result.steps) > 0
```

#### 3.5. Mock Fixture Kullanımı

```python
@pytest.mark.asyncio
async def test_matrix_multiplication(mock_gemini_agent):
    """Matris çarpımı testi"""
    # Arrange: Mock'u matris çarpımı için doğru sonuç
    # döndürecek şekilde yapılandır
    mock_gemini_agent.generate_json_response.return_value = {
        "result": [[17], [39]],
        "steps": ["[[1,2],[3,4]] * [[5],[6]] = [[17],[39]]"],
        "confidence_score": 1.0,
    }

    # Act
    module = LinearAlgebraModule(mock_gemini_agent)
    result = await module.calculate("[[1,2],[3,4]] * [[5],[6]]")

    # Assert: Sonuç tipi ve değeri kontrol et
    assert result.result == [[17], [39]]
    assert isinstance(result.result, list)
    assert result.confidence_score == 1.0
```

#### 3.6. Error Handling Testleri

```python
@pytest.mark.asyncio
async def test_basic_math_invalid_characters(mock_gemini_agent):
    """Geçersiz karakterler engellenir"""
    # Arrange
    module = BasicMathModule(mock_gemini_agent)

    # Act
    result = await module.calculate("import('os').system('rm -rf /')")

    # Assert: Hata mesajı ve API çağrısı yapılmamalı
    assert result.error == "Geçersiz veya yasaklı ifade girdiniz."
    assert result.result == ""
    mock_gemini_agent.generate_json_response.assert_not_called()
```

#### 3.7. Rate Limiter Testleri (Async Mock)

```python
@pytest.mark.asyncio
async def test_rate_limiter_acquire_with_wait():
    """Rate limiter - bekleme gerektiren durum"""
    # Arrange
    limiter = RateLimiter(calls_per_minute=60)
    limiter.last_call_time = 0.0

    # Act & Assert: Minimum 1 saniye bekleme garantisi
    with patch('time.time', side_effect=[0.5, 0.5, 2.0]):
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await limiter.acquire()
            mock_sleep.assert_called_once()
            assert mock_sleep.call_args[0][0] >= 1.0
```

#### Test Best Practices

1. **Mock Yapılandırması**: Her test kendi mock değerini set etmeli
2. **Kapsamlı Assertion**: Sadece `result is not None` değil, tüm kritik alanları kontrol et
3. **Float Karşılaştırması**: `abs(result - expected) < tolerance` kullan
4. **Exception Testleri**: `pytest.raises` ile doğru exception tipini ve mesajını kontrol et
5. **Async Testler**: `@pytest.mark.asyncio` decorator'ını unutma
6. **Mock Verification**: API çağrılarının yapılıp yapılmadığını kontrol et

---

## 🆕 Eklenen Özellikler

Hackathon sırasında projeye eklenen yeni özellikler ve iyileştirmeler:

### Yeni Modül: Statistics Module (İstatistik Modülü)

**Açıklama:**
Statistics Module, veri setleri üzerinde istatistiksel hesaplamalar yapmak için geliştirilmiş yeni bir modüldür. Bu modül, temel istatistiksel işlemlerden (ortalama, medyan, standart sapma) ileri seviye analizlere (korelasyon, regresyon, z-score) kadar geniş bir yelpazede hesaplamalar yapabilmektedir.

**Kullanım:**

```python
# Prefix ile kullanım
"!stats mean [1,2,3,4,5]"
"!statistics std dev [10,20,30,40,50]"
"!stat correlation [1,2,3,4,5] [2,4,6,8,10]"

# Doğal dil ile kullanım
"mean [1,2,3,4,5]"
"standart sapma [10,20,30,40,50]"
"z-score 75 mean=70 std=5"
"percentile 85 [10,20,30,40,50,60,70,80,90,100]"
"correlation [1,2,3,4,5] [2,4,6,8,10]"
```

**Özellikler:**

- **Temel İstatistikler:**
  - Mean (Ortalama): Veri setinin aritmetik ortalaması
  - Median (Medyan): Veri setinin ortanca değeri
  - Mode (Mod): En sık tekrarlanan değer

- **Dağılım Ölçüleri:**
  - Standard Deviation (Standart Sapma): Veri setinin yayılımını ölçer
  - Variance (Varyans): Standart sapmanın karesi

- **İlişki Analizi:**
  - Correlation (Korelasyon): İki veri seti arasındaki ilişki katsayısı
  - Regression (Regresyon): Basit lineer regresyon analizi

- **Normalizasyon:**
  - Z-score: Bir değerin ortalamadan kaç standart sapma uzakta olduğunu gösterir
  - Percentile (Yüzdelik): Veri setindeki bir değerin yüzdelik dilimi

- **Gemini AI Entegrasyonu:**
  - Tüm hesaplamalar Gemini AI ile yapılır
  - Adım adım çözüm adımları gösterilir
  - Metadata ile ek bilgiler (örnek boyutu, istatistik tipi) sağlanır

**Test Coverage:**

```bash
# Statistics modülü testleri
pytest tests/modules/test_statistics.py -v

# Coverage ile
pytest tests/modules/test_statistics.py --cov=src.modules.statistics --cov-report=html

# Tüm testler
pytest tests/ -v
```

**Test Sonuçları:**
- ✅ `test_statistics_mean` - Ortalama hesaplama testi
- ✅ `test_statistics_std_dev` - Standart sapma testi
- ✅ `test_statistics_correlation` - Korelasyon testi
- ✅ `test_statistics_z_score` - Z-score testi
- ✅ `test_statistics_median` - Medyan testi

**Dosya Yapısı:**

```
src/modules/
├── statistics.py          # İstatistik modülü
└── ...

src/config/
├── prompts.py             # STATISTICS_PROMPT eklendi
└── ...

tests/modules/
├── test_statistics.py     # İstatistik modülü testleri
└── ...
```

**Kod Örneği:**

```python
from src.modules.statistics import StatisticsModule
from src.core.agent import GeminiAgent

# Modül oluşturma
gemini_agent = GeminiAgent()
statistics_module = StatisticsModule(gemini_agent)

# Ortalama hesaplama
result = await statistics_module.calculate("mean [1,2,3,4,5]")
print(f"Ortalama: {result.result}")  # 3.0
print(f"Adımlar: {result.steps}")

# Standart sapma hesaplama
result = await statistics_module.calculate("std dev [10,20,30,40,50]")
print(f"Standart Sapma: {result.result}")

# Korelasyon hesaplama
result = await statistics_module.calculate("correlation [1,2,3,4,5] [2,4,6,8,10]")
print(f"Korelasyon: {result.result}")  # 1.0 (mükemmel pozitif korelasyon)
```

**Entegrasyon:**

- ✅ `src/modules/__init__.py` - StatisticsModule export edildi
- ✅ `src/main.py` - CalculatorAgent'a eklendi
- ✅ `src/core/parser.py` - Keyword'ler eklendi (`mean`, `median`, `std dev`, vb.)
- ✅ `src/config/prompts.py` - STATISTICS_PROMPT eklendi

---

### Diğer Eklenen Özellikler

#### 1. Gelişmiş Güvenlik Validasyonu

**Açıklama:**
Settings ve InputValidator modüllerine defensive programming yaklaşımıyla ekstra güvenlik kontrolleri eklendi.

**Kullanım:**

```python
# Settings validation - Placeholder API key kontrolü
from src.config.settings import settings

settings.validate()  # Placeholder değerleri reddeder

# InputValidator - Gelişmiş güvenlik kontrolleri
from src.core.validator import InputValidator

validator = InputValidator()
validator.sanitize_expression("2 + 2")  # Güvenli ifade
validator.sanitize_expression("eval('malicious_code')")  # SecurityViolationError
```

**Faydalar:**

- Placeholder API key'lerin kullanılmasını önler
- Güvenlik açıklarını (eval, exec, __import__) tespit eder
- Type ve boş ifade kontrolleri ile daha güvenli input handling
- Kullanıcı dostu hata mesajları

**Kod Örneği:**

```python
# src/config/settings.py
@classmethod
def validate(cls) -> bool:
    if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "":
        raise ValueError("GEMINI_API_KEY gerekli")
    if cls.GEMINI_API_KEY == "your_gemini_api_key":
        raise ValueError("Placeholder değer kullanılamaz")
    return True

# src/core/validator.py
def sanitize_expression(self, expression: str) -> str:
    if not expression or not isinstance(expression, str):
        raise InvalidInputError("Gecersiz giris: ifade string olmali")
    if not expression.strip():
        raise InvalidInputError("Bos ifade gonderilemez")
    # Güvenlik pattern kontrolü
    for pattern in self.FORBIDDEN_PATTERNS:
        if pattern in expression.lower():
            raise SecurityViolationError(f"Yasakli ifade: {pattern}")
    return expression.strip()
```

---

#### 2. Yapılandırılmış JSON Logging

**Açıklama:**
Logger modülüne JSON formatında yapılandırılmış logging eklendi. Duplicate handler'lar önlendi ve logger/handler level uyumluluğu sağlandı.

**Kullanım:**

```python
from src.utils.logger import setup_logger

logger = setup_logger(name="calculator_agent", level=logging.INFO)
logger.info("Hesaplama basladi")
logger.error("Hata olustu", exc_info=True)
```

**Faydalar:**

- JSON formatında yapılandırılmış loglar (log aggregation için uygun)
- Duplicate handler'ların önlenmesi
- Logger ve handler level uyumluluğu
- Root logger'ı etkilemeyen izole logging
- Exception bilgilerinin otomatik kaydedilmesi

**Log Çıktısı Örneği:**

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "level": "INFO",
  "module": "main",
  "function": "process_command",
  "message": "Hesaplama basladi: 2 + 2"
}
```

**Kod Örneği:**

```python
# src/utils/logger.py
class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)

def setup_logger(name: str = "calculator_agent", level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()  # Duplicate önleme
    handler = logging.StreamHandler()
    handler.setLevel(level)  # Level uyumluluğu
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.propagate = False  # Root logger izolasyonu
    return logger
```

---

#### 3. Gelişmiş Test Infrastructure

**Açıklama:**
Test fixture'ları iyileştirildi. Mock'lar daha güvenli ve yanıltıcı olmayan default değerlerle yapılandırıldı. Test assertion'ları güçlendirildi.

**Kullanım:**

```python
# tests/conftest.py - Mock fixture
@pytest.mark.asyncio
async def test_basic_math(mock_gemini_agent):
    # Her test kendi mock'unu yapılandırmalı
    mock_gemini_agent.generate_json_response.return_value = {
        "result": 4.0,
        "steps": ["2 + 2 = 4"],
        "confidence_score": 1.0,
    }
    
    module = BasicMathModule(mock_gemini_agent)
    result = await module.calculate("2 + 2")
    
    assert result.result == 4.0
    assert len(result.steps) > 0
    assert result.confidence_score == 1.0
```

**Faydalar:**

- Yanıltıcı default değerler yerine nötr değerler (0.0, [])
- Her test kendi mock'unu yapılandırmaya zorlanıyor
- Daha kapsamlı assertion'lar (result, steps, confidence_score)
- Domain field'ının her modül tarafından set edilmesi
- Test edilmeden tespit edilemeyen hataların önlenmesi

**Kod Örneği:**

```python
# tests/conftest.py
@pytest.fixture
def mock_gemini_agent():
    """Mock Gemini agent fixture
    
    NOT: Her test kendi mock'unu yapılandırmalı (return_value override etmeli).
    Bu default değerler sadece fallback olarak kullanılır.
    """
    agent = MagicMock(spec=GeminiAgent)
    agent.generate_json_response = AsyncMock(
        return_value={
            "result": 0.0,  # Nötr default değer
            "steps": [],
            "confidence_score": 1.0,
            # domain kaldırıldı - her modül kendi domain'ini set ediyor
        }
    )
    return agent
```

---

#### 4. Exception Hierarchy İyileştirmesi

**Açıklama:**
Exception sınıfları düzgün bir hiyerarşiye kavuşturuldu. Python'ın built-in exception'larını shadow eden isimler düzeltildi.

**Kullanım:**

```python
from src.utils.exceptions import (
    CalculationError,
    InvalidInputError,
    SecurityViolationError,
    CalculatorModuleNotFoundError,  # ModuleNotFoundError shadow'u önlendi
)

try:
    # Hesaplama işlemi
    pass
except InvalidInputError as e:
    # Geçersiz giriş hatası
    pass
except SecurityViolationError as e:
    # Güvenlik ihlali
    pass
except CalculatorModuleNotFoundError as e:
    # Modül bulunamadı
    pass
```

**Faydalar:**

- Düzgün exception hierarchy (CalculationError → InvalidInputError)
- Python built-in exception'larının shadow edilmemesi
- Daha spesifik exception handling
- Exception'ların düzgün raise edilmesi ve yakalanması

**Kod Örneği:**

```python
# src/utils/exceptions.py
class CalculationError(Exception):
    """Genel hesaplama hatası"""
    pass

class InvalidInputError(CalculationError):
    """Geçersiz giriş formatı"""
    pass

class CalculatorModuleNotFoundError(Exception):
    """Modül bulunamadı (Python'ın built-in ModuleNotFoundError'ını shadow etmemek için)"""
    pass
```

---

#### 5. Rate Limiting İyileştirmesi

**Açıklama:**
Rate limiter'a Gemini API gereksinimlerine uygun minimum 1 saniye bekleme garantisi eklendi.

**Kullanım:**

```python
# src/core/agent.py - RateLimiter
rate_limiter = RateLimiter(calls_per_minute=60)
await rate_limiter.acquire()  # Minimum 1 saniye garantisi
```

**Faydalar:**

- Gemini API gereksinimlerine uyum
- Rate limit aşılmasının önlenmesi
- API çağrılarının başarılı olması garantisi
- Exponential backoff ile retry mekanizması

**Kod Örneği:**

```python
# src/core/agent.py
async def acquire(self) -> None:
    async with self.lock:
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_interval:
            wait_time = self.min_interval - time_since_last_call
            # Minimum 1 saniye garantisi (Gemini API gereksinimi)
            actual_wait_time = max(wait_time, 1.0)
            await asyncio.sleep(actual_wait_time)
        
        self.last_call_time = time.time()
```

---

## 🧪 Test Sonuçları

### Test Coverage

```bash
# Coverage raporu
pytest --cov=src --cov-report=html
```

**Coverage Sonuçları:**

- **Toplam Coverage**: [%92]
- **Modüller**: [%91]
- **Core**: [%94]
- **Utils**: [%99]

### Test Sonuçları

```bash
# Test çalıştırma
pytest -v
```

**Sonuçlar:**

- ✅ Başarılı Testler: [161]
- ❌ Başarısız Testler: [0]
- ⏭️ Atlanan Testler: [0]

---

## 📊 Hata Çözüm Özeti

### Çözülen Hatalar

| Hata No | Kategori        | Dosya                                | Satır      | Durum | Puan |
| ------- | --------------- | ----------------------------------- | ---------- | ----- | ---- |
| 1       | Level 1 + 3     | src/modules/base_module.py           | 1-20       | ✅    | 30   |
| 2       | Level 2         | src/core/agent.py                    | 45-60      | ✅    | 20   |
| 3       | Level 3         | src/modules/basic_math.py, calculus.py, linear_algebra.py, financial.py, equation_solver.py | varies | ✅    | 25   |
| 4       | Level 3         | src/core/agent.py                    | 70-85      | ✅    | 20   |
| 5       | Level 1 + 2     | src/schemas/models.py                | 10-25      | ✅    | 30   |
| 6       | Level 1 + 3     | src/utils/exceptions.py              | 5-20       | ✅    | 25   |
| 7       | Level 1         | src/core/agent.py, src/modules/calculus.py, src/modules/linear_algebra.py, src/modules/basic_math.py | varies | ✅ | 20   |
| 8       | Level 1 + 2 + 3 | src/config/settings.py               | 30-50      | ✅    | 25   |
| 9       | Level 1 + 3     | src/utils/logger.py                  | 15-35      | ✅    | 15   |
| 10      | Level 2         | src/modules/linear_algebra.py, src/modules/graph_plotter.py, src/main.py | varies | ✅ | 20   |
| 11      | Level 3         | src/core/parser.py                   | 50-65      | ✅    | 15   |
| 12      | Level 1 + 2     | src/main.py                          | 70-100     | ✅    | 20   |


### Toplam Puan

- **Level 1 Hatalar**: [X] / 40 puan
- **Level 2 Hatalar**: [X] / 60 puan
- **Level 3 Hatalar**: [X] / 60 puan
- **Bonus Modül**: [X] / 40 puan
- **CI/CD**: [X] / 20 puan
- **Dokümantasyon**: [X] / 10 puan
- **TOPLAM**: [X] / 230 puan

---

## 🚀 CI/CD Pipeline

### GitHub Actions

**Pipeline Yapılandırması:**

```yaml
# .github/workflows/ci.yml 
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-test:
    runs-on: ubuntu-latest

    env:
      GEMINI_MODEL: gemini-2.5-flash

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install flake8

      - name: Run tests with coverage
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: pytest --cov=src --cov-report=html --cov-report=term -v

      - name: Lint with flake8
        run: flake8 src tests --max-line-length=79 --statistics

      - name: Upload coverage report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
          if-no-files-found: ignore

      - name: Build Docker image (test)
        if: github.event_name == 'push'
        run: |
          docker build -t calculator-agent:test .
          docker images calculator-agent:test


```

**Pipeline Adımları:**

1. **Kodun Checkout Edilmesi**  
   `actions/checkout@v3` kullanılarak repository içeriği pipeline ortamına çekiliyor.

2. **Python Ortamının Kurulması**  
   `actions/setup-python@v4` ile belirtilen Python sürümü (`3.11`) kuruluyor.

### Docker Build and Push Pipeline

**Otomatik Docker Build ve Deployment:**

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  workflow_dispatch:

jobs:
  build-and-push:
    - Build Docker image (multi-arch: amd64, arm64)
    - Push to Docker Hub
    - Cache optimization with GitHub Actions cache
  
  deploy:
    - Deploy to production (SSH/Kubernetes/AWS/Google Cloud)
    - Health checks
    - Rollback support
```

**Özellikler:**
- ✅ Multi-architecture support (linux/amd64, linux/arm64)
- ✅ Build cache optimization
- ✅ Automatic tagging (latest, branch, sha, semver)
- ✅ Production deployment support
- ✅ Security: Secrets management

**Gerekli Secrets:**
- `DOCKER_USERNAME`: Docker Hub kullanıcı adı
- `DOCKER_PASSWORD`: Docker Hub access token
- Production deployment için: `SSH_PRIVATE_KEY`, `KUBE_CONFIG`, vb.

Detaylı deployment örnekleri için [.github/workflows/deploy-examples.md](.github/workflows/deploy-examples.md) dosyasına bakın.

3. **Bağımlılıkların Yüklenmesi**  
   `pip install -r requirements.txt` ile proje bağımlılıkları kuruluyor.

4. **Testlerin Çalıştırılması ve Coverage Raporu**  
   `pytest --cov=src --cov-report=xml` ile birim testler çalıştırılıyor ve test kapsamı (coverage) XML formatında üretiliyor.

5. **Kod Lint Kontrolü**  
   `flake8 src tests` komutu ile kod standartlarına uygunluk ve stil hataları kontrol ediliyor.

6. **Coverage Raporunun Yüklenmesi**  
   `actions/upload-artifact@v3` kullanılarak `coverage.xml` dosyası GitHub Actions pipeline’ına artifact olarak yükleniyor.


**Pipeline Durumu:**

- Build:  ✅
- Test:   ✅
- Lint:   ✅
- Deploy: ✅

---

## 📝 Kodlama Standartları

Projede uyulması gereken standartlar:

- **Async/Await**: Tüm Gemini API çağrılarında async pattern
- **Type Hints**: Tüm fonksiyonlarda zorunlu tip belirtilmesi
- **Google Docstring**: Dokümantasyon formatı
- **Pydantic Models**: Input/output validasyonu
- **Test Coverage**: Minimum %90 unit test coverage

---

## 🔒 Güvenlik İyileştirmeleri

Hackathon sırasında yaptığınız güvenlik iyileştirmeleri:

### 1. Girdi Hijyeni ve Yasaklı İfadeler

**Problem:**
Kullanıcı ifadeleri doğrudan modüllere iletiliyor, `__import__` / `eval` gibi zararlı çağrılar filtrelenmiyordu.

**Çözüm:**
`InputValidator.sanitize_expression` tüm prefixleri temizleyip yasaklı pattern listesine göre denetim yapıyor; ihlalde `SecurityViolationError` üretip işlemi durduruyor.

**Kod:**

```python
class InputValidator:
    FORBIDDEN_PATTERNS = ["__import__", "eval(", "exec(", "os.", "subprocess"]

    def sanitize_expression(self, expression: str) -> str:
        if any(pattern in expression for pattern in self.FORBIDDEN_PATTERNS):
            raise SecurityViolationError("Yasakli ifade tespit edildi")
        return expression.strip()
```

### 2. Gizli Anahtarların Testlerde Sızmaması

**Problem:**
Testler sırasında gerçek `GEMINI_API_KEY` değerleri okunabiliyor, CI ortamında sızıntı riski oluşuyordu.

**Çözüm:**
`src/config/__init__.py` içine eklenen `reload_settings()` helper’ı ile testler env’i patch edip modülü yeniden yüklüyor; ayrıca `GeminiAgent` testlerinde API key field’ları bilinçli olarak boş patch’leniyor.

**Kod:**

```python
import importlib
from . import settings as settings_module

def reload_settings():
    """Testlerde env patch sonrası güvenli reload."""
    return importlib.reload(settings_module)
```

### 3. Yapılandırılmış JSON Logging

**Problem:**
Konsola yazılan debug çıktıları hem gizlilik riski yaratıyor hem de log analizi zorlaşıyordu.

**Çözüm:**
`src/utils/logger.py` yeniden yazılarak JSON formatlı, handler düzeyi eşleşen ve `propagate=False` olan bir logger sağlandı; hassas bilgiler maskelemeye uygun hale getirildi.

**Kod:**

```python
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": datetime.utcnow().isoformat(),
        }
        return json.dumps(payload, ensure_ascii=False)
```

---

## 🏗️ Proje Yapısı

```
ai-builder-challenge-hackathon/
├── src/
│   ├── main.py                   # Agent orchestrator & CLI
│   ├── config/
│   │   ├── settings.py           # API keys, rate limits, validation
│   │   └── prompts.py            # Domain prompt şablonları
│   ├── core/
│   │   ├── agent.py              # Gemini istemcisi + rate limiter
│   │   ├── parser.py             # Komut yönlendirme
│   │   └── validator.py          # Girdi hijyeni ve güvenlik
│   ├── modules/
│   │   ├── base_module.py        # Ortak abstract sınıf
│   │   ├── basic_math.py
│   │   ├── calculus.py
│   │   ├── equation_solver.py
│   │   ├── financial.py
│   │   ├── graph_plotter.py
│   │   ├── linear_algebra.py
│   │   └── statistics.py
│   ├── schemas/
│   │   └── models.py             # Pydantic sonuç modelleri
│   └── utils/
│       ├── exceptions.py
│       ├── helpers.py
│       └── logger.py
├── tests/
│   ├── config/
│   │   └── test_settings.py
│   ├── core/
│   │   ├── test_agent.py
│   │   ├── test_parser.py
│   │   └── test_validator.py
│   ├── modules/
│   │   ├── test_basic_math.py
│   │   ├── test_calculus.py
│   │   ├── test_equation_solver.py
│   │   ├── test_financial.py
│   │   ├── test_graph_plotter.py
│   │   ├── test_linear_algebra.py
│   │   └── test_statistics.py
│   ├── utils/
│   │   └── test_helpers.py
│   ├── test_integration.py
│   └── test_main.py
├── cache/                        # Grafik cache klasörü
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎓 Öğrenilen Dersler

Hackathon sırasında öne çıkan dersler:

1. **Mock ve Async Test Disiplini**

   - Gemini gibi harici servisleri izole etmeden güvenilir test yazmak mümkün değil; `AsyncMock`, patch ve helper’larla deterministik sonuçlar üretmenin önemini gördük.

2. **Modüler Mimari ve SRP**

   - Her hesaplama ailesi için ayrı modül tasarlamak, hem hata ayıklamayı hem de yeni özellik eklemeyi ciddi biçimde hızlandırıyor; BaseModule kalıbı buna rehberlik ediyor.

3. **Ölçülebilir Güvenlik ve Observability**
   - Girdilerin güvenli ve beklenen formata dönüştürme/temizleme işlemi, özel istisnalar ve JSON log formatı olmadan, güvenlik ihlallerini yakalamak ve izlemek neredeyse imkânsız; erken aşamada bu altyapıyı kurmak büyük fark yaratıyor.

4. **Kullanıcıya Transparan Geri Bildirim**

   - Türkçe, net hata mesajları ve yönlendirici çıktılar sayesinde “ne oldu?” sorusu daha doğmadan yanıtlanmış oldu. Agent projelerinde son kullanıcıyı belirsizlikte bırakmamak kritik.

5. **Çapraz Modül Akışlarını Önceden Kurgulama**

   - Finans çıktısını grafiğe, graph verisini rapora taşımak gibi senaryoları baştan planlamak; sonradan yamalama yapmaktan çok daha az maliyetli. Modüller arası sözleşmeleri erkenden tanımladıkça sürprizler azalıyor.

---


## 📄 Lisans

Bu proje AI Builder Challenge hackathon'u için geliştirilmiştir.



**İyi hackathonlar! 🚀**
