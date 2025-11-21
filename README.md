<div align="center">

# **Endfield Industrial Protocol Core**

### // 终末地 · 集成工业协议核心 / 资产管理终端

<!-- Status Badges -->

![Status](https://img.shields.io/badge/System_Status-Online-4ade80?style=flat-square)
![Frontend](https://img.shields.io/badge/Nuxt_3-Frontend-00DC82?style=flat-square\&logo=nuxt.js)
![Backend](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square\&logo=fastapi)
![Database](https://img.shields.io/badge/SQLModel-Database-2563eb?style=flat-square)

<p>
基于《明日方舟：终末地》世界观扩展设计，构建一个集 **3D 资产管理 / 实时监控 / 蓝图交互** 为一体的现代化工业 Web 平台。
</p>

<p><i>Last Updated: 2025-11-21 19:30 (ChengDu)</i></p>

</div>

---

## 🏗️ 技术架构 (Tech Stack)

本项目采用 **Monorepo (单仓库)** + **前后端分离** 的现代架构：

| 模块           | 技术栈                            | 说明                  |
| :----------- | :----------------------------- | :------------------ |
| **Frontend** | Nuxt 3 (Vue 3 + TypeScript)    | 轻量 SSR 渲染，工业风 UI    |
| **Backend**  | FastAPI (Python 3.11+)         | 高性能异步接口，自动文档生成      |
| **Database** | SQLModel (SQLite / PostgreSQL) | 结合 Pydantic 的现代 ORM |
| **Package**  | pnpm / pip                     | 前后端依赖管理             |

---

## 🚀 快速开始 (Quick Start)

请严格按照以下步骤配置本地环境：

### **1. 环境准备 (Prerequisites)**

请确保系统已安装：

* **Node.js ≥ 20 (LTS)**
* **Python ≥ 3.10**
* **Git 最新版**

安装 pnpm：

```bash
npm install -g pnpm
```

---

### **2. 克隆仓库 (Clone)**

```bash
git clone https://github.com/The-Endfield-DAM/Endfield-protocol-core.git
cd Endfield-protocol-core
```

---

### **3. 启动后端 (Backend)**

🟢 默认端口：`8000`

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动 FastAPI（热重载）
python -m uvicorn main:app --reload
```

验证接口文档：
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### **4. 启动前端 (Frontend)**

🟢 默认端口：`3000`

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
npm run dev -- --host 0.0.0.0
```

验证前端页面：
👉 [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

## 📂 目录结构 (Structure)

```text
Endfield-protocol-core/
├── backend/                # 后端核心服务 (FastAPI)
│   ├── routers/            # API 路由定义模块
│   ├── .env                # [重要] 环境变量与密钥配置
│   ├── config.py           # 全局配置加载器 (Pydantic)
│   ├── database.py         # 数据库连接与 Session 管理
│   ├── main.py             # 程序主入口 (CORS/LifeCycle)
│   ├── models.py           # SQLModel 数据库模型
│   └── requirements.txt    # Python 依赖清单
│
├── frontend/               # 前端交互界面 (Nuxt 3)
│   ├── assets/css/         # 样式资源 (设计变量/布局样式)
│   ├── components/         # 业务组件 (如 AssetCard)
│   ├── layouts/            # 全局布局模板 (侧边栏/导航)
│   ├── pages/              # 页面路由视图 (首页/上传/设置)
│   ├── public/             # 静态公共资源
│   ├── .npmrc              # pnpm 镜像源配置文件
│   ├── app.vue             # 应用主视图入口
│   ├── nuxt.config.ts      # Nuxt 项目核心配置
│   ├── package.json        # 前端依赖清单
│   └── tsconfig.json       # TypeScript 配置
│
├── .gitignore              # 全局 Git 忽略规则
└── README.md               # 项目总说明书
```

---

## ⚠️ 协作规范 (Collaboration Rules)

> **[!IMPORTANT] 请所有干员务必遵守以下规则，以保证系统稳定性与开发质量。**

### **📌 分支管理**

* `main` 为受保护分支，**禁止直接 push**。
* 新功能请创建独立分支：
  `git checkout -b feat/功能名`
  示例：`feat/login`

### **📌 提交规范 (Commit Style)**

统一使用格式：

```
type: 描述
```

示例：
`feat: 新增资产录入接口`
`fix: 修复数据库连接异常`

### **📌 合并流程 (Pull Request)**

1. 功能完成后提交 PR（Pull Request）
2. 通过组长 Code Review 后方可合并入主分支

---

## 📅 更新日志 (Changelog)

### [v0.2.1] - Cloud Infrastructure Migration
> **Time:** 2025-11-21 21:10
*   **☁️ Database:** 数据库引擎从本地 SQLite 迁移至 **Supabase (PostgreSQL)**，实现云端数据同步。
*   **🔧 Configuration:** 重构后端配置系统 (`config.py`)，集成 Cloudflare R2 对象存储凭证与云数据库连接串。
*   **📦 Dependencies:** 新增 `psycopg2-binary` (PG驱动) 与 `boto3` (S3 SDK) 依赖。
*   **🔒 Security:** 完善环境变量管理，实现敏感密钥与代码库的完全分离。

### [v0.2.0] - UI/UX Protocol Upgrade
> **Time:** 2025-11-21 19:30
*   **✨ New Features:**
    *   引入 **Lucide Vue** 图标库，实现工业风图标系统。
    *   新增 **"呼吸式" 侧边栏 (Collapsible Sidebar)**，支持鼠标悬停自动展开/收起交互。
    *   新增 **Dashboard Hero** 区域，增加动态背景纹理与数据看板。
*   **💄 UI/UX:**
    *   重构 CSS 变量系统 (Design Tokens)，统一管理品牌色与尺寸。
    *   优化布局架构，实现沉浸式全屏布局。
*   **🐛 Bug Fixes:**
    *   修复 Windows 环境下 Nuxt 路径别名 (`~`) 解析错误。
    *   解决前端路由在无后端连接时的阻塞问题 (Lazy Fetch)。

### [v0.1.0] - Architecture Genesis
> **Time:** 2025-11-21 18:10
*   **🏗️ Architecture:** 完成前后端分离架构搭建 (Nuxt3 + FastAPI)。
*   **🔙 Backend:** 集成 SQLModel，实现 SQLite 数据库连接与自动建表。
*   **🔌 API:** 完成 `POST /assets/` (录入) 和 `GET /assets/` (查询) 接口。
*   **🎨 Frontend:** 完成首页 UI Demo，实现前后端数据联调。
*   **🔧 DevOps:** 配置 `.npmrc` 加速国内依赖下载，解决 CORS 跨域限制。

<div align="center">
<br>
<b>Endfield Industries</b><br>
<i>May the connection be stable.</i>
<br><br>
</div>
