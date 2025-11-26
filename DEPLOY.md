# 🐳 Docker Deployment Guide

Bu dokümantasyon, Calculator Agent uygulamasını Docker ile deploy etme adımlarını içerir.

## 📋 Gereksinimler

- Docker (20.10+)
- Docker Compose (1.29+) - Opsiyonel
- Gemini API Key

## 🚀 Hızlı Başlangıç

### 1. Environment Variables Hazırlama

```bash
# .docker.env dosyası oluştur
cp .docker.env.example .docker.env

# .docker.env dosyasını düzenle ve GEMINI_API_KEY'i ekle
nano .docker.env
```

### 2. Docker Image Build Etme

```bash
# Docker image'ı build et
docker build -t calculator-agent:latest .

# Build'i test et
docker run --rm --env-file .docker.env calculator-agent:latest "2 + 2"
```

### 3. Docker Compose ile Çalıştırma (Önerilen)

```bash
# Environment dosyasını hazırla
cp .docker.env.example .docker.env
# .docker.env dosyasını düzenle

# Container'ı başlat
docker-compose up -d

# Logları görüntüle
docker-compose logs -f

# Container'a bağlan (interactive mode için)
docker-compose exec calculator-agent python -m src.main

# Container'ı durdur
docker-compose down
```

## 🔧 Manuel Docker Kullanımı

### Container Oluşturma ve Çalıştırma

```bash
# Container'ı çalıştır (interactive mode)
docker run -it --rm \
  --env-file .docker.env \
  -v $(pwd)/cache:/app/cache \
  -v $(pwd)/logs:/app/logs \
  --name calculator-agent \
  calculator-agent:latest

# Tek komut çalıştırma
docker run --rm \
  --env-file .docker.env \
  calculator-agent:latest "!calculus derivative x^2"

# Arka planda çalıştırma
docker run -d \
  --env-file .docker.env \
  -v $(pwd)/cache:/app/cache \
  -v $(pwd)/logs:/app/logs \
  --name calculator-agent \
  --restart unless-stopped \
  calculator-agent:latest
```

## 🌐 Production Deployment

### Docker Hub'a Push Etme

```bash
# Docker Hub'a login
docker login

# Image'ı tag'le
docker tag calculator-agent:latest yourusername/calculator-agent:latest

# Push et
docker push yourusername/calculator-agent:latest
```

### Production Ortamında Kullanım

```bash
# Docker Hub'dan çek
docker pull yourusername/calculator-agent:latest

# Production'da çalıştır
docker run -d \
  --env-file .docker.env \
  -v /var/app/cache:/app/cache \
  -v /var/app/logs:/app/logs \
  --name calculator-agent \
  --restart always \
  yourusername/calculator-agent:latest
```

## 🔒 Güvenlik Notları

1. **API Key Güvenliği**: `.docker.env` dosyasını asla commit etmeyin
2. **Volume Mounts**: Production'da cache ve logs için uygun izinler ayarlayın
3. **Network**: Gerekirse Docker network kullanarak container'ları izole edin

## 📊 Monitoring ve Logs

```bash
# Container loglarını görüntüle
docker logs calculator-agent

# Real-time log takibi
docker logs -f calculator-agent

# Container durumunu kontrol et
docker ps | grep calculator-agent

# Container içine gir
docker exec -it calculator-agent /bin/bash
```

## 🛠️ Troubleshooting

### Container Başlamıyor

```bash
# Logları kontrol et
docker logs calculator-agent

# Environment variables'ı kontrol et
docker exec calculator-agent env | grep GEMINI

# Container'ı yeniden başlat
docker-compose restart
```

### API Key Hatası

```bash
# .docker.env dosyasını kontrol et
cat .docker.env | grep GEMINI_API_KEY

# Environment variable'ı manuel set et
docker run --rm \
  -e GEMINI_API_KEY=your_key_here \
  calculator-agent:latest "2 + 2"
```

### Cache/Logs Klasörü İzin Sorunları

```bash
# Klasör izinlerini düzelt
sudo chown -R $USER:$USER cache/ logs/
chmod -R 755 cache/ logs/
```

## 📦 Multi-Architecture Build (Opsiyonel)

ARM64 ve AMD64 için build:

```bash
# Buildx setup
docker buildx create --use

# Multi-arch build
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t yourusername/calculator-agent:latest \
  --push .
```

## 🔄 CI/CD Integration

### GitHub Actions ile Otomatik Build ve Push

Proje, GitHub Actions ile otomatik Docker build ve push desteği içerir.

#### Gerekli Secrets

GitHub Repository → Settings → Secrets and variables → Actions:

1. **Docker Hub:**
   - `DOCKER_USERNAME`: Docker Hub kullanıcı adı
   - `DOCKER_PASSWORD`: Docker Hub şifresi veya access token

2. **Production Deployment (Opsiyonel):**
   - `SSH_PRIVATE_KEY`, `SSH_USER`, `SSH_HOST` (SSH deployment için)
   - `KUBE_CONFIG` (Kubernetes için)
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (AWS ECS için)

#### Workflow Tetikleyicileri

- **Push to main**: Otomatik build ve push
- **Tag push (v*)**: Version tag ile build
- **Pull Request**: Sadece build (push yok)
- **Manual**: workflow_dispatch ile manuel tetikleme

#### Kullanım

```bash
# 1. Secrets'ları GitHub'a ekle
# Repository → Settings → Secrets → New repository secret

# 2. Main branch'e push yap
git push origin main

# 3. GitHub Actions otomatik olarak:
#    - Docker image build eder
#    - Docker Hub'a push eder
#    - Production'a deploy eder (yapılandırıldıysa)
```

#### Detaylı Deployment Örnekleri

Detaylı deployment senaryoları için [.github/workflows/deploy-examples.md](.github/workflows/deploy-examples.md) dosyasına bakın.

## 📝 Notlar

- Container interactive mode için `-it` flag'i gerektirir
- Matplotlib non-interactive backend (Agg) kullanır
- Cache ve logs volume mount edilmelidir
- Health check her 30 saniyede bir çalışır

