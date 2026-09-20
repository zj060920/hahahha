#!/usr/bin/env bash
set -e
REPO="${1:-https://github.com/zj060920/hahahha.git}"
BRANCH="${2:-main}"
command -v git >/dev/null || { echo 'Git 未安装'; exit 1; }
command -v gh >/dev/null || { echo 'GitHub CLI 未安装'; exit 1; }
git init
git branch -M "$BRANCH"
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO"
gh auth status
git add .
git commit -m 'Add AI hardware market monitor plugin' || true
git push -u origin "$BRANCH"
echo "上传完成：$REPO"
