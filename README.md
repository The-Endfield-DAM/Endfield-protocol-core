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

<p><i>Last Updated: 2025-11-21 18:30 (Asia/Shanghai)</i></p>

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

## 📂 项目结构 (Directory Structure)

```text
Endfield-protocol-core/
├── backend/                # 后端核心模块
│   ├── routers/            # API 路由
│   ├── models.py           # SQLModel 数据模型
│   ├── database.py         # 连接与 Session 管理
│   ├── config.py           # 环境配置
│   ├── main.py             # 程序入口
│   └── database.db         # SQLite (自动生成)
│
├── frontend/               # 前端模块
│   ├── app.vue             # 主应用入口
│   ├── nuxt.config.ts      # Nuxt 配置文件
│   └── package.json        # 前端依赖
│
├── .gitignore
└── README.md
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


<div align="center">
<br>
<b>Endfield Industries</b><br>
<i>May the connection be stable.</i>
<br><br>
</div>
