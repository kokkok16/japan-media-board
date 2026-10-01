#!/bin/bash

echo "🚀 开始为您一键配置 24/7 日剧 & 电影看板云端自动更新系统..."

# 1. 检查并初始化 Git 仓库
if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

# 2. 自动创建 GitHub Actions 24/7 定时工作流目录和文件
mkdir -p .github/workflows

cat << 'WORKFLOW' > .github/workflows/auto_update.yml
name: 24/7 自动抓取更新日剧 & 电影看板

on:
  schedule:
    # 每天北京时间 08:00 与 20:00 自动触发云端抓取
    - cron: '0 0,12 * * *'
  workflow_dispatch: # 支持网页端手动点击一键更新

jobs:
  build-and-update:
    runs-on: ubuntu-latest
    steps:
      - name: 检出仓库代码
        uses: actions/checkout@v3

      - name: 配置 Python 环境
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: 安装抓取依赖
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4

      - name: 运行爬虫抓取最新日剧/电影数据并生成网页
        run: |
          python code_artifact.py || python run.py

      - name: 自动提交并部署最新网页到 GitHub
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add japan_media_data.json index.html || true
          git commit -m "🤖 [24/7 Auto-Update] 定时更新日剧与电影看板数据 [skip ci]" || exit 0
          git push
WORKFLOW

echo "✅ 24/7 云端定时任务配置完成！"

# 3. 提交本地所有文件
git add .
git commit -m "🎉 初次提交：日剧看板全自动系统"

# 4. 一键自动在 GitHub 上创建云端仓库并开启 Pages 静态网页托管
echo "🌐 正在 GitHub 上自动创建云端仓库并部署网页..."
gh repo create japan-media-board --public --source=. --remote=origin --push
gh repo edit --enable-pages --pages-branch main

echo ""
echo "=========================================================="
echo "🎉 恭喜！一键配置完全成功！"
echo "1. 你的看板现在已实现 24/7 云端自动抓取与更新（即使电脑关机也会运行）。"
echo "2. 每天早上 8 点和晚上 8 点云端服务器会自动拉取最新日剧/电影信息。"
echo "=========================================================="
