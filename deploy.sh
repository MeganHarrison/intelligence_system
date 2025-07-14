#!/bin/bash

echo "🚀 Strategic Dashboard Deployment Helper"
echo "========================================"

# Check if user wants to proceed
read -p "Ready to deploy? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Check if origin is set
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Git remote 'origin' not set."
    echo "Please set up your GitHub repository:"
    echo "1. Create a new repository on GitHub"
    echo "2. Run: git remote add origin https://github.com/yourusername/your-repo.git"
    echo "3. Run this script again"
    exit 1
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy: Strategic Dashboard ready for production"

# Push to GitHub
echo "🔄 Pushing to GitHub..."
git push -u origin main

echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "🌐 Next steps:"
echo "1. Backend: Go to https://railway.app and deploy your backend"
echo "2. Frontend: Go to https://vercel.com and deploy your frontend"
echo "3. Set environment variables in both platforms"
echo "4. Update CORS settings in your backend"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"