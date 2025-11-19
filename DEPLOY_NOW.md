# 🚀 Deploy to Vercel - Quick Guide

## ✅ Cleanup Complete
All test files, backups, and documentation removed. Project is production-ready!

## 📦 What's Included
- **Core Files**: app.py, requirements.txt, vercel.json
- **Models**: Semantic & sentiment analyzers
- **Databases**: 1,480 verses (Thirukkural + Kamba Ramayanam)
- **Frontend**: HTML, CSS, JS
- **Config**: .gitignore, .vercelignore

---

## 🌐 Step 1: Create GitHub Repository

### Option A: Using GitHub Website
1. Go to: https://github.com/new
2. Repository name: `tamil-semantic-analyzer`
3. Description: `Tamil literature semantic analyzer with Thirukkural and Kamba Ramayanam support`
4. Keep it **Public** (or Private if you prefer)
5. **DO NOT** initialize with README (we already have one)
6. Click **Create repository**

### Option B: Using GitHub CLI (if installed)
```powershell
gh repo create tamil-semantic-analyzer --public --source=. --remote=origin --push
```

---

## 📤 Step 2: Push to GitHub

After creating the repository, copy the commands shown on GitHub, or use:

```powershell
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tamil-semantic-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/guhan/tamil-semantic-analyzer.git
git push -u origin main
```

---

## 🚀 Step 3: Deploy to Vercel

### Method 1: Using Vercel Website (Recommended)

1. **Go to Vercel**: https://vercel.com/new
2. **Import Git Repository**:
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose your GitHub account
   - Select `tamil-semantic-analyzer`
3. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. **Environment Variables**: None needed!
5. **Click "Deploy"**

### Method 2: Using Vercel CLI

```powershell
# Install Vercel CLI (if not installed)
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# Set up and deploy? Yes
# Which scope? Your account
# Link to existing project? No
# Project name? tamil-semantic-analyzer
# Directory? ./
# Override settings? No
```

---

## ⏱️ Deployment Time
- **Initial deployment**: 2-5 minutes
- **Subsequent deploys**: 1-2 minutes

---

## 🎉 After Deployment

Vercel will provide you with:
- **Production URL**: `https://tamil-semantic-analyzer.vercel.app`
- **Preview URL**: `https://tamil-semantic-analyzer-git-main-yourname.vercel.app`

### Test Your Deployment
1. Open the URL in your browser
2. Enter a Thirukkural verse:
   ```
   அகர முதல எழுத்தெல்லாம் ஆதி
   பகவன் முதற்றே உலகு
   ```
3. Enter a Kamba verse with character name:
   ```
   இராமன் வனத்திற்கு சென்றார்
   ```

---

## 🔧 Troubleshooting

### If deployment fails:

1. **Check Build Logs**: Click on deployment → "View Function Logs"
2. **Common Issues**:
   - **Memory Error**: Already configured (3008 MB)
   - **Timeout**: Already configured (30 seconds)
   - **Missing dependencies**: All in requirements.txt

### Update Deployment
```powershell
git add .
git commit -m "Update"
git push
```
Vercel auto-deploys on every push!

---

## 📊 Deployment Configuration

Already configured in `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "memory": 3008,
        "maxDuration": 30
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

---

## 🎯 Next Steps

1. ✅ Create GitHub repository
2. ✅ Push code to GitHub
3. ✅ Deploy to Vercel
4. ✅ Get your live URL
5. ✅ Share with users!

**Your Tamil Semantic Analyzer will be live at:**
`https://YOUR-PROJECT-NAME.vercel.app`

---

## 💡 Tips

- **Custom Domain**: Add in Vercel dashboard → Settings → Domains
- **Analytics**: Enable in Vercel dashboard → Analytics
- **Environment**: Automatic HTTPS, CDN, global deployment
- **Updates**: Just `git push` - auto-deploys!

---

## ✅ Production Ready!
- 🎯 1,480 verses loaded
- 🔍 Structure-based book detection
- 📚 Thirukkural + Kamba Ramayanam
- 🚀 100% offline-capable
- ⚡ Fast response times

**🎉 Ready to deploy!**
