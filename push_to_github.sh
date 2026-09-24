#!/usr/bin/env bash
set -euo pipefail

# Check if target repository URL argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: ./push_to_github.sh <GITHUB_REPO_URL>"
    echo "Example: ./push_to_github.sh https://github.com/my-org/my-codemender-demo.git"
    exit 1
fi

REPO_URL="$1"

echo "Initializing Git repository..."
git init
git branch -M main

echo "Adding demo files..."
git add .

echo "Creating initial commit..."
git commit -m "Initial commit: CodeMender Vulnerable Python Demo App & CI/CD Pipeline"

echo "Setting remote URL to $REPO_URL..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

echo "Pushing to GitHub (main branch)..."
git push -u origin main

echo "=========================================================================="
echo "Successfully initialized and pushed demo repository to GitHub!"
echo "Next step: Ensure WIF secrets (WIF_PROVIDER, WIF_SERVICE_ACCOUNT, GCP_PROJECT_ID)"
echo "are configured in your GitHub repository Settings -> Secrets and variables."
echo "=========================================================================="
