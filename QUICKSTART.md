# 🚀 Quick Deployment Commands

## Step 1: Create GitHub Repository
Go to: https://github.com/new
- Name: `tamil-semantic-analyzer`
- Public repository
- Do NOT initialize with README

## Step 2: Connect and Push to GitHub

```powershell
# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/tamil-semantic-analyzer.git

# Rename branch to main
git branch -M main

# Push code to GitHub
git push -u origin main
```

## Step 3: Deploy to Vercel

1. Go to: https://vercel.com
2. Sign up with GitHub account
3. Click "New Project"
4. Select `tamil-semantic-analyzer` repository
5. Click "Deploy"
6. Wait 2-5 minutes
7. Get your live URL: `https://your-project.vercel.app`

## ✅ Deployment Checklist

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub (`git push`)
- [ ] Signed up on Vercel
- [ ] Imported GitHub repository to Vercel
- [ ] Deployment successful
- [ ] Tested live URL
- [ ] Shared link with users

## 🔗 Important URLs

- **GitHub**: https://github.com
- **Vercel**: https://vercel.com  
- **Your Repo**: https://github.com/YOUR_USERNAME/tamil-semantic-analyzer
- **Your Live App**: https://your-project.vercel.app

## 📋 What's Included

- ✅ 1,480 verses database
- ✅ Thirukkural (1,330 verses)
- ✅ Kamba Ramayanam (150 verses)
- ✅ Semantic search API
- ✅ Sentiment analysis
- ✅ Web interface
- ✅ 100% offline capable

## 🔄 Update Deployment

Whenever you make changes:

```powershell
git add .
git commit -m "Your update message"
git push
```

Vercel automatically redeploys on every push!

## 📞 Need Help?

Read the complete guide: **DEPLOY.md**

---

**Total deployment time: ~10 minutes** ⏱️
