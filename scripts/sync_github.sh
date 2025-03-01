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
if [ -z "$GITHUB_REPO_URL" ]; then
    log_error "GITHUB_REPO_URL is not set."
    exit 1
fi

log_message "Fetching from GitHub"
git remote add github "$GITHUB_REPO_URL" || git remote set-url github "$GITHUB_REPO_URL"
git fetch github

# Check if there are changes on GitHub that aren't in GitLab
log_message "Checking for changes on GitHub"
if git rev-list HEAD..github/master | grep -q .; then
    log_error "GitHub contains changes not present in GitLab."
    log_error "Please pull these changes into GitLab before syncing."
    exit 1
fi

# Push to GitHub
log_message "Pushing to GitHub"
git push github master:master

log_message "Sync completed successfully"
