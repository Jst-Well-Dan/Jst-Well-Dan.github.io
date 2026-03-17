# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Dan 的个人博客，Hugo + PaperMod 主题，部署到 GitHub Pages（`https://jst-well-dan.github.io/`）。用途：知识外化

## 常用命令

```bash
# 本地开发预览（含草稿）
hugo server -D

# 生产构建
hugo --gc --minify

# 新建文章（使用 archetype 模板）
hugo new posts/<slug>/index.md
```

## 仓库结构

```
content/posts/<slug>/     每篇文章是独立的 Page Bundle
  index.md                文章正文 + YAML front matter
  image-*.png             文章引用的图片，与 index.md 同目录（相对路径引用）

static/css/dan-brand.css  品牌色覆盖（仅链接和代码块左边框）
themes/PaperMod/          git submodule，不要手动修改主题文件
.github/workflows/        hugo.yml — push to main 自动构建并部署到 Pages
```

## 文章规范

**Front matter 必填字段：**
```yaml
---
title: "文章标题"
date: 2026-01-01
description: "一句话摘要"
categories: ["工具与技术"]   # 三选一：AI与学习 / 金融与投资 / 工具与技术
tags: ["标签1", "标签2"]
---
```

**图片引用：** 使用相对路径 `![](image-name.png)`，图片文件放在同一 Page Bundle 目录下。不要使用 Obsidian 的 `![[image.png]]` 语法。

**封面图：** 每篇文章第一行放封面图 `![](cover-image.png)`，封面图由用户提供（暖琥珀品牌色系）。

## 品牌样式

"Gallery 逻辑"：PaperMod 主题保持中性灰，品牌色仅施加于链接和代码块左边框，使封面图的品牌色更突出。

- 亮色模式链接色：`#b45309`（暖琥珀）
- 暗色模式链接色：`#f97316`（明橙）
- 扩展主题样式只在 `static/css/dan-brand.css` 中修改，不动主题源码。

## 部署

push 到 `main` 分支后，GitHub Actions 自动构建并部署。工作流使用 Hugo Extended v0.145.0，checkout 时递归拉取 submodule。

Pages 设置：仓库 Settings → Pages → Source 选 **GitHub Actions**。
