#!/bin/bash

set -e

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to log errors
log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
}

log_message "Starting GitHub sync"

# Check for required environment variables
if [ -z "$GITHUB_OPN_API_REPO_URL" ]; then
    log_error "GITHUB_OPN_API_REPO_URL is not set."
    exit 1
fi

# Ensure we have the proper Git setup in CI environment
log_message "Setting up Git environment"
git config -l
log_message "Current directory: $(pwd)"
log_message "Git status:"
git status || echo "Git status failed"

# Fix detached head state if needed
if git rev-parse --abbrev-ref HEAD | grep -q "HEAD"; then
    log_message "In detached HEAD state, checking out master branch"
    git checkout master || git checkout -b master
fi

log_message "Current branch: $(git rev-parse --abbrev-ref HEAD)"

# Add GitHub as remote
log_message "Setting up GitHub remote"
if git remote | grep -q "github"; then
    log_message "Remote 'github' already exists, updating URL"
    git remote set-url github "$GITHUB_OPN_API_REPO_URL"
else
    log_message "Adding 'github' remote"
    git remote add github "$GITHUB_OPN_API_REPO_URL"
fi

log_message "Fetching from GitHub"
git fetch github

# Check if there are changes on GitHub that aren't in GitLab
log_message "Checking for changes on GitHub"
if git rev-list HEAD..github/master 2>/dev/null | grep -q .; then
    log_error "GitHub contains changes not present in GitLab."
    log_error "Please pull these changes into GitLab before syncing."
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
log_message "Pushing branch '$CURRENT_BRANCH' to GitHub"

# Push to GitHub
git push github "$CURRENT_BRANCH":master

log_message "Sync completed successfully"
