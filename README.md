# Endfield Industrial Protocol Core
### // 终末地集成工业协议 / 资产管理终端

> **System Status:** 🟢 Online (Alpha)  
> **Last Updated:** 2025-11-21 18:10 (Asia/Shanghai)

本项目为基于《明日方舟：终末地》世界观衍生的工业资产管理系统（Fan Project）。旨在构建一个集 3D 资产管理、实时数据监控与交互式蓝图构建于一体的现代化 Web 应用。

---

## 🏗️ 技术架构 (Tech Stack)

本项目采用 **Monorepo (单仓库)** 架构，前后端分离开发。

| 模块 | 技术栈 | 说明 |
| :--- | :--- | :--- |
| **Frontend** | **Nuxt 3** (Vue 3 + TypeScript) | 极速 SSR 渲染，工业风 UI 组件 |
| **Backend** | **FastAPI** (Python 3.11+) | 高性能异步接口，自动生成文档 |
| **Database** | **SQLModel** (SQLite / PostgreSQL) | 结合 Pydantic 的现代化 ORM |
| **Package** | **pnpm** (Frontend) / **pip** (Backend) | 依赖包管理 |

---

## 🚀 快速开始 (Quick Start)

请各位干员（开发人员）严格按照以下步骤部署本地开发环境。

### 1. 环境准备 (Prerequisites)
- **Node.js:** v20.0.0+ (LTS)
- **Python:** v3.10+
- **Git:** 最新版
- **包管理器:** 请预先安装 pnpm (`npm install -g pnpm`)

### 2. 获取代码
```bash
git clone https://github.com/The-Endfield-DAM/Endfield-protocol-core.git
cd Endfield-protocol-core
3. 启动后端 (Backend)
后端运行在 http://127.0.0.1:8000。
code
Bash
# 打开一个新的终端窗口
cd backend

# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务 (热重载模式)
python -m uvicorn main:app --reload
✅ 验证： 访问 http://127.0.0.1:8000/docs 查看 API 文档。
4. 启动前端 (Frontend)
前端运行在 http://127.0.0.1:3000。
code
Bash
# 打开另一个终端窗口
cd frontend

# 1. 安装依赖 (使用 pnpm)
pnpm install

# 2. 启动开发服务器
npm run dev -- --host 0.0.0.0
✅ 验证： 访问 http://127.0.0.1:3000 查看资产列表页面。
📂 目录结构 (Structure)
code
Text
Endfield-protocol-core/
├── backend/                # 后端核心逻辑
│   ├── routers/            # API 路由定义
│   ├── models.py           # 数据库模型 (SQLModel)
│   ├── database.py         # 数据库连接与会话管理
│   ├── config.py           # 全局配置 (Env loader)
│   ├── main.py             # 程序入口 (CORS配置)
│   └── database.db         # 本地 SQLite 数据库 (自动生成)
├── frontend/               # 前端界面逻辑
│   ├── app.vue             # 主应用入口 (当前包含资产列表 Demo)
│   ├── nuxt.config.ts      # Nuxt 配置
│   └── package.json        # 前端依赖定义
├── .gitignore              # 全局 Git 忽略配置
└── README.md               # 项目说明书
⚠️ 协作规范 (Collaboration Rules)
为了保证系统的稳定性，请遵守以下协议：
分支管理：
main 分支为受保护分支，严禁直接 Push。
开发新功能请切出新分支：git checkout -b feat/功能名 (例: feat/login)。
代码提交：
提交信息请遵循规范：type: 描述 (例: feat: 新增资产录入接口, fix: 修复CORS跨域问题)。
合并流程：
开发完成后，请在 GitHub 发起 Pull Request (PR)。
等待组长 (Tech Lead) Code Review 通过后方可合并。
依赖管理：
前端安装新包：pnpm add 包名。
后端安装新包：pip install 包名 后，务必执行 pip freeze > requirements.txt 更新依赖表。
📅 更新日志 (Changelog)
[v0.1.0] - 2025-11-21
Architecture: 完成前后端分离架构搭建 (Nuxt3 + FastAPI)。
Backend: 集成 SQLModel，实现 SQLite 数据库连接与自动建表。
API: 完成 POST /assets/ (录入) 和 GET /assets/ (查询) 接口。
Frontend: 完成首页 UI 开发 (终末地工业风格)，实现前后端数据联调。
DevOps: 配置 .npmrc 加速国内依赖下载，解决 CORS 跨域限制。
Endfield Industries.
May the connection be stable.