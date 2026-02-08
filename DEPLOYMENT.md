# 🚀 Deployment Guide

This guide shows how to deploy TrendScope to production for your hackathon demo or real-world use.

---

## Option 1: Local Development (Fastest)

**Best for:** Hackathon demos, testing

### Backend
```bash
cd backend
python app.py
# Runs on http://localhost:5000
```

### Frontend
```bash
cd frontend
python -m http.server 8000
# Visit http://localhost:8000
```

**Pros:** 
- Zero setup
- Instant changes
- No costs

**Cons:**
- Not accessible externally
- Needs to keep terminal open

---

## Option 2: Render (Free Tier)

**Best for:** Live demos, simple deployments

### Backend Deployment

1. **Create `render.yaml`:**

```yaml
services:
  - type: web
    name: trendscope-api
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 10000
```

2. **Add to requirements.txt:**
```bash
gunicorn==21.2.0
```

3. **Connect to GitHub:**
   - Push code to GitHub
   - Connect Render to your repo
   - Deploy automatically

4. **Get URL:**
   - `https://trendscope-api.onrender.com`

### Frontend Deployment

Use Render Static Sites or Netlify:

1. **Update API URL in `script.js`:**
```javascript
const API_BASE_URL = 'https://trendscope-api.onrender.com';
```

2. **Deploy:**
   - Drag/drop `frontend/` folder to Netlify
   - Or connect GitHub repo

**Cost:** Free  
**Deploy time:** 5 minutes  
**Uptime:** Good for demos

---

## Option 3: Railway (Easy with Database)

**Best for:** Production-ready deployments

### 1. Install Railway CLI
```bash
npm i -g @railway/cli
railway login
```

### 2. Deploy Backend
```bash
cd backend
railway init
railway up
```

### 3. Add Environment Variables
```bash
railway variables set DEBUG=False
railway variables set PORT=8000
```

### 4. Get Public URL
```bash
railway domain
# Returns: https://trendscope-production.up.railway.app
```

### 5. Deploy Frontend
- Use Vercel or Netlify
- Update API URL

**Cost:** $5/month  
**Deploy time:** 3 minutes  
**Uptime:** Production-grade

---

## Option 4: DigitalOcean App Platform

**Best for:** Scalable production

### Backend Setup

1. **Create `app.yaml`:**

```yaml
name: trendscope
services:
  - name: api
    github:
      repo: yourusername/trendscope
      branch: main
      deploy_on_push: true
    source_dir: /backend
    run_command: gunicorn app:app
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: PORT
        value: "8080"
```

2. **Deploy:**
   - Connect GitHub
   - Select repo
   - Auto-deploy

### Frontend Setup

1. **Create `staticwebapp.config.json`:**

```json
{
  "routes": [
    {
      "route": "/api/*",
      "rewrite": "https://trendscope-api-xxxxx.ondigitalocean.app"
    }
  ]
}
```

2. **Deploy:**
   - Use DigitalOcean Spaces + CDN
   - Or connect to Vercel/Netlify

**Cost:** $5-12/month  
**Deploy time:** 10 minutes  
**Uptime:** Enterprise-grade

---

## Option 5: AWS (Advanced)

**Best for:** Enterprise deployments

### Backend: AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize:**
```bash
cd backend
eb init -p python-3.11 trendscope-api
```

3. **Create environment:**
```bash
eb create trendscope-prod
```

4. **Deploy:**
```bash
eb deploy
```

### Frontend: AWS S3 + CloudFront

1. **Build static site:**
```bash
cd frontend
# No build needed, already static
```

2. **Upload to S3:**
```bash
aws s3 sync . s3://trendscope-frontend
```

3. **Setup CloudFront CDN**

4. **Update API URL:**
```javascript
const API_BASE_URL = 'https://api.trendscope.com';
```

**Cost:** ~$10-30/month  
**Deploy time:** 30 minutes  
**Uptime:** 99.99%

---

## Option 6: Docker (Any Platform)

**Best for:** Containerized deployments

### Create `Dockerfile` (Backend)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV PORT=8000
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:8000"
    environment:
      - DEBUG=False
      - PORT=8000
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    volumes:
      - ./frontend:/usr/share/nginx/html
    ports:
      - "80:80"
    restart: unless-stopped
```

### Deploy

```bash
docker-compose up -d
```

**Can deploy to:**
- DigitalOcean Droplets
- AWS ECS
- Google Cloud Run
- Azure Container Instances

---

## Environment Variables

### Production `.env`

```env
# Backend Configuration
PORT=8000
DEBUG=False

# CORS (update with your frontend URL)
ALLOWED_ORIGINS=https://trendscope.com,https://www.trendscope.com

# GenAI API Keys (when integrated)
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx

# Database (if added)
DATABASE_URL=postgresql://user:pass@host:5432/trendscope

# Security
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

---

## Performance Optimization

### Backend

1. **Use Gunicorn:**
```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
```

2. **Add caching:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/platforms')
@cache.cached(timeout=3600)
def get_platforms():
    # ...
```

3. **Add rate limiting:**
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/analyze-trend')
@limiter.limit("10 per minute")
def analyze_trend():
    # ...
```

### Frontend

1. **Minify assets:**
```bash
# CSS
npm install -g clean-css-cli
cleancss -o styles.min.css styles.css

# JS
npm install -g terser
terser script.js -o script.min.js -c -m
```

2. **Add CDN:**
```html
<!-- Use CDN for Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

3. **Enable GZIP:**
```nginx
# nginx.conf
gzip on;
gzip_types text/css application/javascript;
```

---

## Monitoring & Analytics

### Backend Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/analyze-trend', methods=['POST'])
def analyze_trend():
    logger.info(f"Analysis request: {request.json}")
    # ...
```

### Error Tracking (Sentry)

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0
)
```

### Analytics (Google Analytics)

```html
<!-- Add to index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXX');
</script>
```

---

## SSL/HTTPS Setup

### Option 1: Let's Encrypt (Free)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d trendscope.com -d www.trendscope.com

# Auto-renew
sudo certbot renew --dry-run
```

### Option 2: Cloudflare (Free + CDN)

1. Point domain to Cloudflare
2. Enable "Full (Strict)" SSL
3. Auto HTTPS enabled

---

## Domain Setup

### 1. Buy Domain
- Namecheap, Google Domains, Cloudflare

### 2. Configure DNS

```
Type    Name    Value
A       @       YOUR_SERVER_IP
A       www     YOUR_SERVER_IP
CNAME   api     trendscope-api.onrender.com
```

### 3. Update CORS

```python
# backend/app.py
CORS(app, origins=[
    'https://trendscope.com',
    'https://www.trendscope.com'
])
```

---

## Deployment Checklist

### Pre-Deploy
- [ ] Test locally
- [ ] Update API URLs
- [ ] Set environment variables
- [ ] Enable error logging
- [ ] Add rate limiting
- [ ] Minify frontend assets

### Deploy
- [ ] Push to production
- [ ] Verify health endpoint
- [ ] Test full workflow
- [ ] Check CORS
- [ ] Monitor logs

### Post-Deploy
- [ ] Setup SSL
- [ ] Configure domain
- [ ] Add monitoring
- [ ] Setup backups (if using DB)
- [ ] Test from multiple devices

---

## Recommended Setup for Hackathon

**Best balance of ease + reliability:**

1. **Backend:** Render (free tier)
2. **Frontend:** Netlify (free tier)
3. **Domain:** Cloudflare (free)
4. **Monitoring:** Sentry (free tier)

**Total cost:** $0  
**Deploy time:** 15 minutes  
**Reliability:** Good for demos

---

## Troubleshooting

### "Application Error" on Render

Check `render.yaml` paths are correct:
```yaml
buildCommand: cd backend && pip install -r requirements.txt
startCommand: cd backend && gunicorn app:app
```

### CORS Errors

Update `app.py`:
```python
CORS(app, resources={
    r"/*": {"origins": "*"}  # For development only!
})
```

### Frontend not connecting

1. Check API_BASE_URL in `script.js`
2. Verify backend is running
3. Check browser console for errors

---

**Ready to deploy?** Start with Render + Netlify for the quickest path to a live demo!
