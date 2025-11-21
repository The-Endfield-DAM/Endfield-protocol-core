<div align="center">

# Endfield Industrial Protocol Core
### // 终末地集成工业协议 / 资产管理终端

<!-- Status Badges -->
![Status](https://img.shields.io/badge/System_Status-Online-4ade80?style=flat-square)
![Vue](https://img.shields.io/badge/Frontend-Nuxt_3-00DC82?style=flat-square&logo=nuxt.js)
![Python](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)
![Database](https://img.shields.io/badge/Database-SQLModel-2563eb?style=flat-square)

<p>
本项目为基于《明日方舟：终末地》世界观衍生的工业资产管理系统。
<br>
旨在构建一个集 3D 资产管理、实时数据监控与交互式蓝图构建于一体的现代化 Web 应用。
</p>

<p>
<i>Last Updated: 2025-11-21 18:30 (Asia/Shanghai)</i>
</p>

</div>

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

请各位干员严格按照以下步骤部署本地开发环境。

1. 环境准备 (Prerequisites)
确保本地已安装以下基础环境：
*   **Node.js:** v20.0.0+ (LTS)
*   **Python:** v3.10+
*   **Git:** 最新版

**安装包管理器 pnpm：**

```bash
npm install -g pnpm
```

2. 获取代码 (Clone)

```bash
git clone https://github.com/The-Endfield-DAM/Endfield-protocol-core.git
cd Endfield-protocol-core
```

3. 启动后端 (Backend)

🟢 运行端口: 8000

请打开一个新的终端窗口，执行以下命令：

```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务 (热重载模式)
python -m uvicorn main:app --reload
```

✅ 验证： 访问 http://127.0.0.1:8000/docs 查看 API 文档。

4. 启动前端 (Frontend)

🟢 运行端口: 3000

请打开另一个终端窗口，执行以下命令：

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖 (使用 pnpm)
pnpm install

# 3. 启动开发服务器
npm run dev -- --host 0.0.0.0
```

✅ 验证： 访问 http://127.0.0.1:3000 查看资产列表页面。

📂 目录结构 (Structure)

```text
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
```

⚠️ 协作规范 (Collaboration Rules)
[!IMPORTANT]
为了保证系统的稳定性，请务必遵守以下协议：

分支管理：
*   `main` 分支为受保护分支，严禁直接 Push。
*   开发新功能请切出新分支：`git checkout -b feat/功能名` (例: `feat/login`)。
**代码提交：**
*   提交信息请遵循规范：`type: 描述` (例: `feat: 新增资产录入接口`)。
**合并流程：**
*   开发完成后，请在 GitHub 发起 Pull Request (PR)。
*   等待组长 Code Review 通过后方可合并。
<div align="center">
<b>Endfield Industries.</b><br>
<i>May the connection be stable.</i>
</div>
```