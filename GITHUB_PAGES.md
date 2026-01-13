# GitHub Pages Deployment (Free Static RSS)

Deploy your RSS feed using **GitHub Actions + GitHub Pages** - completely free, no server needed!

## ✅ How It Works

**GitHub Pages serves static files only**, but we can use **GitHub Actions** to:
1. Run Python script every 30 minutes
2. Fetch topics from groups.io API
3. Generate `feed.xml` file
4. Commit and push to GitHub
5. Serve via GitHub Pages

**Result:** Free, auto-updating RSS feed at `https://yourusername.github.io/psp-rss-reader/feed.xml`

---

## 🚀 Setup (10 minutes)

### 1. Fork/Clone the Repository

Already done if you're reading this! ✓

### 2. Add Your API Key as GitHub Secret

⚠️ **Important:** Never commit your API key to the repository!

1. **Go to your repo on GitHub**
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret:**
   - Name: `GROUPS_IO_API_KEY`
   - Value: `your_64_character_api_key_here`
4. **Save**

### 3. Enable GitHub Pages

1. **Settings** → **Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `gh-pages` / `(root)`
4. **Save**

### 4. Trigger First Build

**Option A: Push a commit**
```bash
git commit --allow-empty -m "Trigger GitHub Actions"
git push
```

**Option B: Manual trigger**
1. Go to **Actions** tab
2. Click "Update RSS Feed"
3. **Run workflow** → **Run workflow**

### 5. Wait ~2 minutes

- GitHub Actions will run
- Generate `feed.xml`
- Deploy to Pages
- Your feed will be live!

### 6. Access Your Feed

Your RSS feed URL:
```
https://yourusername.github.io/psp-rss-reader/feed.xml
```

Replace `yourusername` with your actual GitHub username.

---

## 📱 Add to RSS Reader

### iPhone/iPad (NetNewsWire)
1. Open NetNewsWire
2. Add Feed → `https://yourusername.github.io/psp-rss-reader/feed.xml`
3. Done! Updates every 30 minutes automatically

### Android (Feeder)
1. Open Feeder
2. + → Add Feed → `https://yourusername.github.io/psp-rss-reader/feed.xml`
3. Done!

---

## ⚙️ How It Works (Technical)

### GitHub Actions Workflow (`.github/workflows/update-feed.yml`)

```yaml
on:
  schedule:
    - cron: '*/30 * * * *'  # Every 30 minutes
  workflow_dispatch:        # Manual trigger
```

**What it does:**
1. Checks out repo
2. Installs Python + dependencies
3. Runs `generate_rss_feed.py` with your API key
4. Commits `feed.xml` if changed
5. Deploys to GitHub Pages

### The Generated Feed

- Static XML file
- Contains ~50 most recent topics
- Includes full message content
- Standard RSS 2.0 format
- Updates every 30 minutes

---

## 🎨 Customize

### Change Update Frequency

Edit `.github/workflows/update-feed.yml`:

```yaml
schedule:
  - cron: '*/15 * * * *'  # Every 15 minutes
  # - cron: '0 * * * *'   # Every hour
  # - cron: '0 */6 * * *' # Every 6 hours
```

### Change Topics Per Group

Edit the workflow file, add environment variable:

```yaml
env:
  GROUPS_IO_API_KEY: ${{ secrets.GROUPS_IO_API_KEY }}
  TOPICS_PER_GROUP: 20  # Change from 10 to 20
```

### Customize Landing Page

Edit `index.html` - it's served at your root URL:
```
https://yourusername.github.io/psp-rss-reader/
```

---

## 📊 Pros & Cons

### ✅ Pros

- **100% Free** (GitHub Pages + Actions)
- **No server needed**
- **Auto-updates** every 30 minutes
- **HTTPS** included
- **Simple** - just push to git
- **Reliable** - GitHub infrastructure

### ⚠️ Cons

- **30-minute delay** minimum (GitHub Actions limit)
- **No on-demand refresh** (can manually trigger)
- **2,000 GitHub Actions minutes/month** limit (plenty for this!)
- **No web reader** (just the XML feed)
- **Static only** (no fancy UI like the FastAPI version)

---

## 🆚 GitHub Pages vs Cloud Hosting

| Feature | GitHub Pages | Render/Railway |
|---------|--------------|----------------|
| **Cost** | Free | Free |
| **Setup** | Medium | Easy |
| **Auto-update** | Every 30min | Real-time |
| **Web Reader** | No | Yes |
| **Server needed** | No | No |
| **HTTPS** | ✅ | ✅ |
| **Best for** | Simple RSS | Full features |

**Recommendation:**
- Use **GitHub Pages** if you just want the RSS feed
- Use **Render/Railway** if you want the web reader too

---

## 🔧 Troubleshooting

### Actions not running?

**Check:**
1. Actions enabled? **Settings → Actions → Allow all actions**
2. Workflow file in `.github/workflows/`?
3. API key secret set correctly?

**View logs:**
- **Actions** tab → Click latest run → View logs

### Feed not updating?

**Check:**
1. GitHub Actions completed successfully?
2. Wait 2-3 minutes after Actions run
3. Clear browser cache: `Ctrl+Shift+R` or `Cmd+Shift+R`

### "Invalid API key" error

**Fix:**
1. Go to **Settings → Secrets**
2. Delete `GROUPS_IO_API_KEY`
3. Re-add with correct key
4. Re-run workflow

### 404 on feed.xml

**Check:**
1. GitHub Pages enabled? **Settings → Pages**
2. Deployed from `gh-pages` branch?
3. Wait 2-3 minutes after first deploy
4. Try: `https://yourusername.github.io/psp-rss-reader/` (with trailing slash)

---

## 🎯 Best Practices

### 1. Keep Your API Key Secret

- ✅ Store in GitHub Secrets
- ❌ Never commit to repo
- ❌ Never share in issues/PRs

### 2. Monitor Actions Usage

- Free tier: 2,000 minutes/month
- Each run: ~1 minute
- 30-min frequency: ~1,440 runs/month = ~1,440 minutes
- **You're safe!** Plenty of headroom

### 3. Test Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export GROUPS_IO_API_KEY="your_key_here"

# Test generation
python3 generate_rss_feed.py

# Check feed.xml created
ls -lh feed.xml
```

---

## 🚀 Advanced: Custom Domain

**Want `rss.yourdomain.com` instead of GitHub URL?**

1. **Buy domain** (or use free: Freenom, Cloudflare Pages)

2. **Add CNAME file:**
   ```bash
   echo "rss.yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

3. **Configure DNS:**
   - Type: `CNAME`
   - Name: `rss`
   - Value: `yourusername.github.io`

4. **Enable in GitHub:**
   - Settings → Pages
   - Custom domain: `rss.yourdomain.com`
   - Enforce HTTPS: ✅

5. **Feed URL now:**
   ```
   https://rss.yourdomain.com/feed.xml
   ```

---

## 💡 Tips

- **Test workflow:** Use "workflow_dispatch" to manually trigger
- **Check logs:** Actions tab shows all runs and errors
- **RSS validators:** https://validator.w3.org/feed/ to check your feed
- **Monitor:** Star your repo to get GitHub notifications

---

## 📚 Resources

- **GitHub Actions docs:** https://docs.github.com/en/actions
- **GitHub Pages docs:** https://docs.github.com/en/pages
- **Cron syntax:** https://crontab.guru/

---

## 🎉 You're Done!

Your RSS feed is now:
- ✅ Auto-updating every 30 minutes
- ✅ Hosted for free on GitHub
- ✅ Accessible from anywhere
- ✅ HTTPS enabled
- ✅ No server maintenance needed

**Feed URL:** `https://yourusername.github.io/psp-rss-reader/feed.xml`

Add it to your favorite RSS reader and enjoy! 🚀
