# Open Source & Free Forever Hosting Options

For those who want truly open source solutions or "always free" tiers (not just trial credits).

## 🌟 Best Open Source Self-Hosting Platforms

### 1. Coolify ⭐ RECOMMENDED

**What it is:** Open source, self-hostable alternative to Heroku/Netlify/Vercel

**Why it's great:**
- ✅ 100% open source (Apache 2.0 license)
- ✅ Beautiful web UI (like Railway/Render)
- ✅ One-click deployments from GitHub
- ✅ Automatic HTTPS with Let's Encrypt
- ✅ Built-in monitoring and logs
- ✅ Supports Docker, static sites, databases

**Setup (20 minutes):**

1. **Get a free server** (see options below)

2. **Install Coolify:**
   ```bash
   curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
   ```

3. **Access web UI:**
   - Go to `http://your-server-ip:8000`
   - Complete setup wizard

4. **Deploy your RSS reader:**
   - Add GitHub repository
   - Set environment variable: `GROUPS_IO_API_KEY`
   - Deploy!

**Where to run Coolify (free):**
- Oracle Cloud Always Free (best - see below)
- Hetzner Cloud (€4.49/month, not free but cheap)
- Your own Raspberry Pi at home

**Links:**
- Website: https://coolify.io
- GitHub: https://github.com/coollabsio/coolify
- Docs: https://coolify.io/docs

---

### 2. CapRover

**What it is:** Open source PaaS (Platform as a Service) you can self-host

**Features:**
- ✅ Open source (Apache 2.0)
- ✅ Web UI for deployments
- ✅ One-click app installs
- ✅ Automatic HTTPS
- ✅ Built on Docker

**Setup:**

```bash
# On your server
docker run -p 80:80 -p 443:443 -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /captain:/captain \
  caprover/caprover
```

**Links:**
- Website: https://caprover.com
- GitHub: https://github.com/caprover/caprover

---

### 3. Dokku

**What it is:** Lightweight open source PaaS (like mini-Heroku)

**Features:**
- ✅ Open source (MIT license)
- ✅ Git push to deploy
- ✅ Very lightweight
- ✅ Plugin system

**Setup:**

```bash
# On Ubuntu server
wget https://raw.githubusercontent.com/dokku/dokku/v0.30.0/bootstrap.sh
sudo DOKKU_TAG=v0.30.0 bash bootstrap.sh
```

**Deploy:**

```bash
# On your local machine
git remote add dokku dokku@your-server:psp-rss-reader
git push dokku main
```

**Links:**
- Website: https://dokku.com
- GitHub: https://github.com/dokku/dokku

---

## ☁️ Free Forever Cloud Providers

### 1. Oracle Cloud Always Free ⭐ BEST VALUE

**What you get (FREE FOREVER):**
- 2 AMD VMs (1/8 OCPU, 1GB RAM each) OR
- 4 ARM VMs (1 OCPU, 6GB RAM each - MUCH BETTER!)
- 200GB storage
- 10TB outbound bandwidth/month
- **No credit card expiration - truly free!**

**Perfect for:**
- Running Coolify/CapRover
- Multiple apps
- Seriously generous

**Setup:**

1. **Create account:** https://cloud.oracle.com/free
2. **Create Always Free VM:**
   - Compute → Instances → Create Instance
   - Image: Ubuntu 22.04
   - Shape: Ampere (ARM) - 4 OCPUs, 24GB RAM (FREE!)
3. **Install Coolify** (see above)
4. **Deploy your RSS reader**

**Pros:**
- ✅ Actually free forever (not a trial)
- ✅ Very generous resources
- ✅ ARM instances are powerful
- ✅ Oracle won't delete it

**Cons:**
- ⚠️ UI is complex
- ⚠️ Need to configure firewall rules

---

### 2. Google Cloud Always Free

**What you get (FREE FOREVER):**
- 1 f1-micro VM (0.6GB RAM)
- 30GB HDD storage
- 1GB outbound bandwidth/month (to Americas)

**Limitations:**
- Must be in specific regions (us-west1, us-central1, us-east1)
- Limited bandwidth

**Good for:** Small projects, testing

---

### 3. AWS Free Tier

**What you get:**
- t2.micro or t3.micro (1GB RAM)
- 750 hours/month for 12 months
- Then you pay (~$8-10/month)

**Limitation:** Only free for 12 months

---

## 🏠 Self-Host at Home (100% Free)

### Raspberry Pi + Cloudflare Tunnel

**What you need:**
- Raspberry Pi ($35-50 one-time)
- Internet connection
- Cloudflare account (free)

**Setup:**

1. **Install Ubuntu on Raspberry Pi**

2. **Install your RSS reader:**
   ```bash
   git clone https://github.com/yourusername/psp-rss-reader.git
   cd psp-rss-reader
   pip install -r requirements.txt
   # Create .env with your API key
   python3 fastapi_rss_server.py
   ```

3. **Install Cloudflare Tunnel (free HTTPS, no port forwarding!):**
   ```bash
   # Install cloudflared
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
   sudo dpkg -i cloudflared-linux-arm64.deb

   # Authenticate
   cloudflared tunnel login

   # Create tunnel
   cloudflared tunnel create psp-rss

   # Route traffic
   cloudflared tunnel route dns psp-rss psp-rss.yourdomain.com

   # Run tunnel
   cloudflared tunnel run psp-rss
   ```

4. **Access from anywhere:**
   - Your URL: `https://psp-rss.yourdomain.com/feed.xml`
   - Free HTTPS
   - No port forwarding needed!

**Pros:**
- ✅ 100% free (after Pi cost)
- ✅ Complete control
- ✅ No monthly costs
- ✅ Learn self-hosting

**Cons:**
- ⚠️ Requires hardware
- ⚠️ Need stable internet
- ⚠️ You're the sysadmin

---

## 📊 Comparison: Open Source Options

| Option | Cost | Complexity | Control | Best For |
|--------|------|------------|---------|----------|
| **Coolify on Oracle** | Free | Medium | Full | Best overall |
| **CapRover** | Free* | Medium | Full | Docker fans |
| **Dokku** | Free* | Low | Full | Simplicity |
| **Raspberry Pi** | $35 | High | Full | Learning |
| **Render.com** | Free | Low | Limited | Easy start |

*Requires a server (Oracle free tier, or paid VPS)

---

## 🎯 Recommended Path

### For Most People:
**Oracle Cloud (free forever) + Coolify**

1. Create Oracle Cloud account (free)
2. Create Always Free ARM VM (powerful!)
3. Install Coolify (one command)
4. Deploy from GitHub (point and click)
5. Get free domain from Cloudflare
6. Enjoy!

### For Developers:
**Oracle Cloud + Dokku**

- More control
- Git-based deployments
- Lightweight

### For Complete Beginners:
**Start with Render.com**

- Not open source, but easiest
- Upgrade to Oracle + Coolify later when comfortable

---

## 🚀 Step-by-Step: Oracle Cloud + Coolify

**Total time: 30 minutes**

### 1. Create Oracle Cloud Account

1. Go to https://cloud.oracle.com/free
2. Sign up (requires credit card for verification, but won't charge)
3. Verify email

### 2. Create Always Free VM

1. **Create VM:**
   - Click: Compute → Instances → Create Instance
   - Name: `coolify-server`
   - Image: Ubuntu 22.04
   - Shape: **Ampere (ARM)** - select "Always Free eligible"
   - Choose: 4 OCPUs, 24GB RAM (yes, this is FREE!)
   - Download SSH keys

2. **Configure Firewall:**
   - Security Lists → Add Ingress Rules:
     - Port 80 (HTTP)
     - Port 443 (HTTPS)
     - Port 8000 (Coolify UI)
     - Port 6001 (Coolify websockets)

3. **Note your Public IP**

### 3. Install Coolify

```bash
# SSH into your server
ssh -i your-key.pem ubuntu@your-server-ip

# Install Coolify (one command!)
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash

# Wait 5 minutes for installation
```

### 4. Access Coolify

1. Go to: `http://your-server-ip:8000`
2. Create admin account
3. Complete setup wizard

### 5. Deploy Your RSS Reader

1. **In Coolify UI:**
   - Resources → New → GitHub App
   - Connect your GitHub account
   - Select `psp-rss-reader` repo

2. **Configure:**
   - Environment: `GROUPS_IO_API_KEY=your_key_here`
   - Port: 8000
   - Deploy!

3. **Get URL:**
   - Coolify will give you: `http://your-server-ip/feed.xml`
   - Or configure custom domain

### 6. Add Custom Domain (Optional)

1. Get free domain: https://www.freenom.com
2. Point DNS to your Oracle VM IP
3. Coolify automatically sets up HTTPS!

**Done! You now have:**
- ✅ Free forever hosting
- ✅ Full control
- ✅ Open source platform
- ✅ HTTPS
- ✅ Powerful ARM server

---

## 💡 Tips

### Save Money:
- Oracle Cloud ARM instances are FREE and powerful
- Cloudflare Tunnel is FREE (no need for paid VPS)
- Freenom domains are FREE (or use Cloudflare)

### Stay Open Source:
- Coolify: Open source
- Dokku: Open source
- CapRover: Open source
- Your RSS reader: Open source

### Get Help:
- Coolify Discord: https://coollabs.io/discord
- Oracle Cloud docs: https://docs.oracle.com/en-us/iaas/
- This project's GitHub Issues

---

## 🔒 Security Notes

When self-hosting:
- ✅ Keep Ubuntu updated: `sudo apt update && sudo apt upgrade`
- ✅ Use SSH keys (no passwords)
- ✅ Configure firewall properly
- ✅ Use Cloudflare for DDoS protection
- ✅ Enable automatic security updates

---

## 📚 Additional Resources

**Coolify:**
- Tutorial: https://www.youtube.com/watch?v=taJlPG82Ucw
- Docs: https://coolify.io/docs

**Oracle Cloud:**
- Always Free: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- ARM instances guide: https://blogs.oracle.com/cloud-infrastructure/post/arm-vms

**Cloudflare Tunnel:**
- Setup guide: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

---

**Bottom line:** You can host this RSS reader 100% FREE using entirely open source tools. Oracle's Always Free tier + Coolify is the sweet spot! 🎉
