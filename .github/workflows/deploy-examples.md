# Production Deployment Örnekleri

Bu dosya, `.github/workflows/docker.yml` içindeki deployment adımları için detaylı örnekler içerir.

## 🔐 Gerekli Secrets

GitHub Repository → Settings → Secrets and variables → Actions bölümüne eklenmesi gereken secrets:

### Docker Hub
- `DOCKER_USERNAME`: Docker Hub kullanıcı adı
- `DOCKER_PASSWORD`: Docker Hub şifresi veya access token

### SSH Deployment
- `SSH_PRIVATE_KEY`: SSH private key
- `SSH_USER`: SSH kullanıcı adı
- `SSH_HOST`: SSH host adresi

### Kubernetes
- `KUBE_CONFIG`: Base64 encoded kubeconfig dosyası

### AWS ECS
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key

## 📋 Deployment Senaryoları

### 1. SSH ile Remote Server

```yaml
- name: Setup SSH
  uses: webfactory/ssh-agent@v0.7.0
  with:
    ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

- name: Deploy via SSH
  run: |
    ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SSH_HOST }} << 'EOF'
      cd /opt/calculator-agent
      docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
      docker-compose down
      docker-compose up -d
      docker system prune -f
    EOF
```

### 2. Kubernetes Deployment

```yaml
- name: Setup kubectl
  uses: azure/setup-kubectl@v3
  with:
    version: 'latest'

- name: Configure kubectl
  run: |
    echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
    export KUBECONFIG=kubeconfig

- name: Deploy to Kubernetes
  run: |
    kubectl set image deployment/calculator-agent \
      calculator-agent=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
    kubectl rollout status deployment/calculator-agent --timeout=5m
```

### 3. AWS ECS (Fargate)

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v2
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v1

- name: Build and push to ECR
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: ${{ steps.login-ecr.outputs.registry }}/calculator-agent:latest

- name: Deploy to ECS
  run: |
    aws ecs update-service \
      --cluster calculator-cluster \
      --service calculator-agent \
      --force-new-deployment \
      --region us-east-1
```

### 4. Google Cloud Run

```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v1
  with:
    credentials_json: ${{ secrets.GCP_SA_KEY }}

- name: Set up Cloud SDK
  uses: google-github-actions/setup-gcloud@v1

- name: Build and push to GCR
  run: |
    gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/calculator-agent:latest

- name: Deploy to Cloud Run
  run: |
    gcloud run deploy calculator-agent \
      --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/calculator-agent:latest \
      --platform managed \
      --region us-central1
```

### 5. Azure Container Instances

```yaml
- name: Azure Login
  uses: azure/login@v1
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}

- name: Build and push to ACR
  run: |
    az acr build --registry ${{ secrets.ACR_NAME }} \
      --image calculator-agent:latest .

- name: Deploy to ACI
  run: |
    az container create \
      --resource-group ${{ secrets.RESOURCE_GROUP }} \
      --name calculator-agent \
      --image ${{ secrets.ACR_NAME }}.azurecr.io/calculator-agent:latest \
      --cpu 1 --memory 1.5 \
      --registry-login-server ${{ secrets.ACR_NAME }}.azurecr.io \
      --registry-username ${{ secrets.ACR_USERNAME }} \
      --registry-password ${{ secrets.ACR_PASSWORD }}
```

## 🚀 Kullanım

1. İlgili deployment senaryosunu seçin
2. Gerekli secrets'ları GitHub'a ekleyin
3. `.github/workflows/docker.yml` dosyasındaki ilgili bölümün yorumlarını kaldırın
4. Production environment'ı GitHub'da oluşturun (Settings → Environments)

## 🔒 Güvenlik Notları

- Secrets'ları asla kod içine yazmayın
- Production environment için approval gerektirebilirsiniz
- SSH key'leri için sadece read-write gereken minimum izinleri verin
- Cloud provider credentials için IAM role'leri kullanın

