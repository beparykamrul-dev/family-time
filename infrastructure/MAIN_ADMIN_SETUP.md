# ISP-OS Main Admin Infrastructure Complete Setup

## 🎯 Multi-Cloud Architecture Overview

Enterprise-grade distributed infrastructure for ISP-OS main admin panel with advanced features:

### Cloud Providers
- **Oracle Cloud** (Primary): us-phoenix-1, VM.Standard.E4.Flex
- **AWS** (Secondary): us-east-1, c6i.2xlarge
- **GCP** (Tertiary): us-central1, c2-standard-4

### CDN & Traffic Routing
- **Cloudflare Tunnel**: Encrypted secure tunnel from origin to edge
- **Bunny.net CDN**: Cost-effective global edge caching
- **Fastly CDN**: Premium with instant purge and custom VCL
- **Multi-cloud failover**: Automatic routing to healthy backend

### Advanced Caching Strategy
- **OpenResty + Nginx**: Origin-pull with aggressive caching
- **Compression**: Zstandard (zstd), Brotli, transparent gzip
- **Redis Cluster**: Distributed session and metric caching
- **Cache Zones**: Static (365d), API (5-30m), Reports (24h)

### Private Networking
- **ZeroTier**: Overlay VPN mesh network
- **Tailscale**: Modern WireGuard-based VPN (alternative)
- **Keepalived**: HA/VRRP with < 1s failover
- **Netmaker**: Web dashboard for mesh management
- **Syncthing**: Configuration synchronization

### Advanced Features
- **Terraform**: Infrastructure as Code for multi-cloud
- **Ansible**: Automated configuration management
- **Kubernetes (K3s)**: On-premises control plane
- **Proxmox Cluster**: Virtualization for critical components
- **OpenResty**: Lua scripting for custom proxy logic
- **Kernel Bypass**: Optional DPDK for ultra-low latency

### Monitoring & Observability
- **Prometheus**: Metrics collection
- **Grafana**: Real-time dashboards
- **Loki**: Log aggregation and analysis
- **Promtail**: Distributed log shipping

---

## 🚀 Quick Start Guide

### Prerequisites
```bash
sudo apt update && sudo apt install -y \
  terraform ansible docker.io docker-compose \
  python3-pip git curl wget

# Verify installations
terraform version && ansible --version && docker --version
```

### Step 1: Clone and Setup
```bash
git clone https://github.com/beparykamrul-dev/family-time.git
cd family-time

# Create environment file
cp infrastructure/.env.example infrastructure/.env
# Edit with your cloud credentials
nano infrastructure/.env
```

### Step 2: Deploy Infrastructure (Terraform)
```bash
cd infrastructure/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Get outputs
terraform output -json > ../inventory/infrastructure.json
```

### Step 3: Configure Servers (Ansible)
```bash
cd infrastructure

# Create inventory from Terraform outputs
terraform output admin_primary_public_ip
terraform output admin_secondary_public_ip
terraform output admin_tertiary_public_ip

# Update inventory file
nano ansible/inventory/hosts.yml

# Run playbook
ansible-playbook ansible/main-admin.yml -v
```

### Step 4: Deploy Docker Stack
```bash
ssh ubuntu@<admin_primary_ip>
cd /opt/admin-platform

docker-compose -f docker-compose.admin.yml pull
docker-compose -f docker-compose.admin.yml up -d

# Verify services
docker-compose -f docker-compose.admin.yml ps
```

### Step 5: Setup Mesh Networking
```bash
# On primary server
ssh ubuntu@<admin_primary_ip> "zerotier-cli join <NETWORK_ID>"

# Authorize in ZeroTier control panel
# https://my.zerotier.com

# Verify connectivity
ssh ubuntu@<admin_primary_ip> "zerotier-cli listnetworks"
```

### Step 6: Configure DNS & SSL
```bash
# SSL certificates (Let's Encrypt recommended)
sudo certbot certonly --standalone -d admin.isp-os.com

# Cloudflare DNS setup
# Add CNAME: admin.isp-os.com → admin-tunnel.isp-os.com
# Or A record pointing to primary IP

# Deploy Cloudflare Tunnel
cloudflared tunnel login
cloudflared tunnel create admin-tunnel
```

---

## 🔍 Verification Checklist

```bash
#!/bin/bash
echo "=== Admin Infrastructure Verification ==="

# Check services
echo "\n[1] Checking services running..."
docker-compose ps | grep -E "(admin-api|postgres|redis|prometheus|grafana)"

# Check API health
echo "\n[2] Checking API health..."
curl -sk https://admin.isp-os.com/health

# Check database
echo "\n[3] Checking database..."
docker exec admin-postgres pg_isready -U admin_user

# Check Redis
echo "\n[4] Checking Redis..."
docker exec redis-admin-cache redis-cli ping

# Check Prometheus
echo "\n[5] Checking Prometheus..."
curl -s http://localhost:9090/-/healthy

# Check Grafana
echo "\n[6] Checking Grafana..."
curl -s http://localhost:3001/api/health | grep -o '"database":"ok"'

# Check ZeroTier
echo "\n[7] Checking ZeroTier mesh..."
sudo zerotier-cli listnetworks

# Check Nginx cache
echo "\n[8] Checking Nginx cache..."
curl -I https://admin.isp-os.com/static/admin.bundle.js | grep "X-Cache-Status"

echo "\n=== Verification Complete ==="
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────┐
│      Global Admin Users             │
└────────────┬────────────────────────┘
             │
    ┌────────▼────────┬──────────────┐
    │ Cloudflare      │  Bunny.net   │
    │ Tunnel + WAF    │  + Fastly    │
    └────────┬────────┴──────────────┘
             │
    ┌────────▼──────────────────┐
    │  OpenResty Nginx Proxy    │
    │  (Caching + Compression)  │
    └────────┬──────────┬───────┘
             │          │
   ┌─────────▼──┐   ┌───▼─────────┐
   │ Oracle     │   │ AWS + GCP   │
   │ Primary    │   │ Secondary   │
   │ (FastAPI)  │   │ (Failover)  │
   └─────────┬──┘   └───┬─────────┘
             │          │
    ┌────────▼──────────▼──────┐
    │  Keepalived VRRP (HA)    │
    │  Virtual IP: 10.0.0.10   │
    └────────┬──────────┬──────┘
             │          │
   ┌─────────▼──┐   ┌───▼──────────┐
   │ ZeroTier   │   │ Tailscale    │
   │ Mesh VPN   │   │ VPN (Alt)    │
   └─────────┬──┘   └───┬──────────┘
             │          │
    ┌────────▼──────────▼──────────┐
    │   Backend Services Stack     │
    │ ├─ PostgreSQL (Primary+Rep)  │
    │ ├─ Redis Cluster (Cache)     │
    │ ├─ Admin API (FastAPI)       │
    │ └─ Monitoring (Prom+Grafana) │
    └─────────────────────────────┘
```

---

## 🛠️ Infrastructure Components

### Docker Compose Services
1. **nginx-reverse-proxy** - OpenResty reverse proxy with Lua scripting
2. **admin-api** - FastAPI backend for admin operations
3. **postgres** - PostgreSQL 16 with HA replication
4. **redis-cluster** - Redis 7 for distributed caching
5. **zerotier** - ZeroTier overlay network
6. **netmaker** - Mesh network dashboard
7. **keepalived** - VRRP high availability
8. **syncthing** - Configuration synchronization
9. **prometheus** - Metrics collection
10. **grafana** - Dashboards and visualization
11. **loki** - Log aggregation
12. **promtail** - Log shipping

### Terraform Modules
- `oracle/compute` - Oracle Cloud VM provisioning
- `aws/ec2` - AWS instance deployment
- `google/compute` - GCP instance deployment
- `cloudflare/zone` - DNS and tunnel setup
- `aws/nlb` - Network load balancer
- `aws/acm` - SSL certificate management

### Ansible Playbooks
- `main-admin.yml` - Main deployment playbook
- Roles:
  - `geerlingguy.docker` - Docker installation
  - `nginx-proxy` - Nginx/OpenResty setup
  - `redis-cache` - Redis cluster setup
  - `postgresql` - Database configuration
  - `zerotier-mesh` - ZeroTier network join
  - `netmaker-setup` - Netmaker agent setup
  - `keepalived-ha` - VRRP configuration
  - `syncthing-config` - Config sync setup
  - `monitoring` - Prometheus + Grafana

---

## 📈 Performance Optimization

### Caching Strategy
```
Static Assets:  365 days (immutable)
API Responses:  5-30 minutes (varies)
Dashboard:      10 minutes
Reports:        24 hours
Realtime:       No cache
```

### Compression
- **Zstandard (zstd)**: 60-70% reduction, low CPU
- **Brotli**: 20% better than gzip, good browser support
- **Transparent**: Applied automatically at reverse proxy

### Rate Limiting
- Admin API: 1000 req/s per server
- Standard API: 100 req/s per IP
- Reports: 20 req/s per IP

---

## 🔐 Security Features

- **HTTPS/TLS 1.3**: All connections encrypted
- **HSTS**: HTTP Strict Transport Security
- **RBAC**: Role-based access control in API
- **JWT Tokens**: Secure authentication (1h expiry)
- **Rate Limiting**: DDoS protection
- **Network Isolation**: ZeroTier private mesh
- **Database Encryption**: At-rest and in-transit
- **Audit Logging**: All admin actions logged

---

## 🚨 Troubleshooting

### Services Not Starting
```bash
# Check logs
docker-compose logs -f admin-api
docker-compose logs -f admin-nginx

# Restart service
docker-compose restart admin-api
```

### High Latency
```bash
# Check cache hit ratio
curl -I https://admin.isp-os.com/static/admin.bundle.js | grep X-Cache-Status

# Check upstream health
nginx -T | grep upstream
```

### Database Connection Issues
```bash
# Test database
docker exec admin-postgres psql -U admin_user -d admin_db -c "SELECT 1"

# Check replication
docker exec admin-postgres psql -U admin_user -c "SELECT * FROM pg_stat_replication;"
```

---

## 📞 Support & Documentation

- Deployment Guide: See [MAIN_ADMIN_SETUP.md](./MAIN_ADMIN_SETUP.md)
- Docker Compose: See [docker-compose.admin.yml](./docker-compose.admin.yml)
- Nginx Config: See [nginx/admin.conf](./nginx/admin.conf)
- Terraform Code: See [terraform/main-admin.tf](./terraform/main-admin.tf)
- Ansible Playbook: See [ansible/main-admin.yml](./ansible/main-admin.yml)

---

**Last Updated**: 2026-05-28
**Maintained By**: ISP-OS Team
