# ISP-OS Setup Guide

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 8GB+ RAM
- 20GB+ disk space

### Installation Steps

#### 1. Clone Repository
```bash
git clone https://github.com/beparykamrul-dev/family-time.git
cd family-time
```

#### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

#### 3. Start Services
```bash
docker-compose up -d
```

#### 4. Verify Installation
```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Access Applications

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | N/A |
| Backend API | http://localhost:8000 | N/A |
| API Docs | http://localhost:8000/docs | N/A |
| Prometheus | http://localhost:9090 | N/A |
| Grafana | http://localhost:3001 | admin/admin123 |

## Development

### Backend Development
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Frontend Development
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## Troubleshooting

### Database Connection Issues
```bash
# Check database container
docker-compose logs db

# Rebuild database
docker-compose down -v
docker-compose up -d
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

## Production Deployment

### Security Checklist
- [ ] Update all credentials in .env
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Setup backup strategy
- [ ] Configure monitoring alerts
- [ ] Review CORS settings
- [ ] Enable database backups

### Scaling
- Use load balancers (Nginx, HAProxy)
- Implement database replication
- Use CDN for static assets
- Configure caching strategies
- Monitor resource usage

## Support

For issues:
1. Check logs: `docker-compose logs <service>`
2. Review documentation
3. Create GitHub issue
