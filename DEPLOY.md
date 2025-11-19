# 🚀 Tamil Semantic Analyzer - Deployment Guide

## Quick Deploy to Vercel

This guide will help you deploy the Tamil Semantic & Sentiment Analyzer to Vercel for free hosting.

## 📋 Prerequisites

1. **GitHub Account** - [Sign up here](https://github.com/join)
2. **Vercel Account** - [Sign up here](https://vercel.com/signup) (free tier)
3. **Git installed** on your computer

## 🎯 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in the details:
   - **Repository name**: `tamil-semantic-analyzer` (or your choice)
   - **Description**: "Tamil Literature Semantic & Sentiment Analyzer"
   - **Visibility**: Public (recommended) or Private
   - **Do NOT** initialize with README (we already have one)
4. Click **"Create repository"**
5. **Copy the repository URL** (e.g., `https://github.com/YOUR_USERNAME/tamil-semantic-analyzer.git`)

### Step 2: Push Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Tamil Semantic Analyzer with 1,480 verses"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/tamil-semantic-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 3: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and **Sign Up** (use your GitHub account for easier integration)

2. Click **"New Project"** or **"Add New..."** → **"Project"**

3. **Import Git Repository**:
   - Click **"Import Git Repository"**
   - Select your GitHub repository: `tamil-semantic-analyzer`
   - If you don't see it, click **"Adjust GitHub App Permissions"** and grant access

4. **Configure Project**:
   - **Framework Preset**: Other (Vercel will auto-detect from vercel.json)
   - **Root Directory**: `./` (leave as is)
   - **Build Command**: (leave empty, serverless deployment)
   - **Output Directory**: (leave empty)

5. **Environment Variables** (Optional):
   - No environment variables needed for this project

6. Click **"Deploy"**

### Step 4: Wait for Deployment

- Vercel will:
  1. Clone your repository
  2. Install dependencies from `requirements.txt`
  3. Build the serverless function
  4. Deploy to global CDN

- This takes **2-5 minutes**

### Step 5: Access Your Live App

Once deployed, you'll see:
- ✅ **Production URL**: `https://your-project-name.vercel.app`
- Click the URL to open your live application!

## 🔗 Your Live Links

After deployment, you'll have:

1. **Production URL**: `https://tamil-semantic-analyzer.vercel.app` (or similar)
2. **GitHub Repository**: `https://github.com/YOUR_USERNAME/tamil-semantic-analyzer`

## ⚙️ Vercel Configuration (vercel.json)

Already configured for you:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "functions": {
    "app.py": {
      "memory": 3008,
      "maxDuration": 30
    }
  }
}
```

## 📊 What's Deployed

- ✅ **1,480 verses** (1,330 Thirukkural + 150 Kamba Ramayanam)
- ✅ **Semantic search** with fuzzy matching
- ✅ **Sentiment analysis** for Tamil text
- ✅ **Web interface** (HTML/CSS/JS)
- ✅ **REST API** endpoint at `/analyze`

## 🔄 Updating Your Deployment

Whenever you make changes:

```powershell
# Add changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push

# Vercel will automatically redeploy!
```

## 🎨 Customizing Your Domain

On Vercel dashboard:

1. Go to your project
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain (e.g., `tamil-analyzer.com`)
4. Follow DNS configuration instructions

## 🐛 Troubleshooting

### Build Fails

**Issue**: Dependencies not installing
**Solution**: Check `requirements.txt` has all dependencies

### Function Timeout

**Issue**: Request takes too long
**Solution**: Already configured with `maxDuration: 30` seconds

### Out of Memory

**Issue**: Not enough memory
**Solution**: Already configured with `memory: 3008` MB (max on free tier)

### Static Files Not Loading

**Issue**: CSS/JS not found
**Solution**: Check paths are relative (e.g., `/static/css/style.css`)

## 📞 Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **GitHub Issues**: Create an issue in your repository

## ✅ Deployment Checklist

- [ ] GitHub account created
- [ ] Vercel account created  
- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] Project imported to Vercel
- [ ] Deployment successful
- [ ] Live URL accessible
- [ ] API endpoint working (`/analyze`)
- [ ] Web interface loading correctly

## 🎉 Success!

Your Tamil Semantic Analyzer is now live and accessible worldwide!

Share your link:
- **Production**: `https://your-project.vercel.app`
- **GitHub**: `https://github.com/YOUR_USERNAME/tamil-semantic-analyzer`

---

**Made with ❤️ for Tamil Literature**
