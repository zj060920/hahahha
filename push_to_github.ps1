param([string]$Repo='https://github.com/zj060920/hahahha.git',[string]$Branch='main')
$ErrorActionPreference='Stop'
if (!(Get-Command git -ErrorAction SilentlyContinue)){throw '请先安装 Git'}
if (!(Get-Command gh -ErrorAction SilentlyContinue)){throw '请先安装 GitHub CLI (gh)'}
git init
git branch -M $Branch
git remote remove origin 2>$null
git remote add origin $Repo
gh auth status
git add .
git commit -m 'Add AI hardware market monitor plugin' 2>$null
git push -u origin $Branch
Write-Host "上传完成：$Repo"
