# Changelog (更新档案)

All notable changes to the **Endfield Industrial Protocol Core** project will be documented in this file.
本项目的所用重要更新均记录于此档案中。

---

## 📅 更新日志 (Changelog)

### [v0.4.4.0] - Mass Transmission & Purge Protocol
> **Time:** 2025-11-24 19:50
*   **📦 Batch Operations (大宗操作协议):**
    *   **Batch Upload:** 上传页面支持 **多文件拖拽/选择**。重构了传输核心，实现了串行任务调度，PRTS 动画现可实时反馈总体进度 (e.g., `SYNCING (3/10)...`)。
    *   **Batch Delete:** Wiki 页面新增 **多选模式** 与 **底部悬浮操作栏**。后端新增接口，支持一次性销毁多个资产（数据库+R2同步删除）。
    *   **Batch Download:** 前端实现并发下载队列，支持一键获取所有选中资产。
*   **🗑️ Asset Lifecycle (资产全生命周期):**
    *   **Deletion:** 补全了文件管理的最后一环。实装了 **红色荧光风格** 的删除确认弹窗，统一了危险操作的视觉警示体系。
    *   **Download Fix:** 修复了点击下载按钮变为浏览器预览的问题。后端 `generate_presigned_url` 现强制注入 `Content-Disposition: attachment` 响应头，并修复了中文文件名的编码乱码问题。
*   **💄 Interaction Polish (交互打磨):**
    *   **Wiki UI:** 重构文件列表项，将单一入口拆分为 `[播放]`、`[下载]`、`[删除]` 独立功能区，提升操作效率。
    *   **Visual Consistency:** 确保所有新增弹窗与按钮均符合 Endfield 工业设计语言。

### [v0.4.3.0] - Identity Protocol & Console Patch
> **Time:** 2025-11-24 16:55

* **🆔 Profile Management (身份管理协议):**
    * **Atomized Editing:** 重构个人档案卡片, 实现行内编辑代号与点击头像上传功能。
    * **Image Cropping:** 集成 `vue-cropperjs`，实现头像上传时的专业级裁剪交互。
    * **Data Persistence:** 修复用户头像上传后无法正确显示的问题，后端接口现已正确返回临时签名后的 `avatar_url`。

* **🎛️ Personal Console (个人终端):**
    * **UI Differentiation:** 针对管理员与普通干员设计了差异化的控制台面板（绿色激活态 vs 黄色待机态）。
    * **Visual Enhancement:** 优化控制台视觉细节，增加扫描线动效与呼吸灯状态指示。

* **🐛 Stability & Fixes:**
    * **Crash Fix:** 修复数据刷新时因异步时序导致的前端崩溃问题。
    * **Schema Fix:** 修复数据库与后端模型中用户表缺失字段导致上传 500 错误的问题。

### [v0.4.2.0] - Tactical Mobile & UX Overhaul
> **Time:** 2025-11-23 20:00
*   **📱 Mobile Adaptation (移动端适配):**
    **本次移动端适配取消了重写元素的方案，体验不佳之处请见谅**
    *   **Strategy Shift:** 确立“强制横屏”交互规范，放弃传统的竖屏流式布局，以保证工业界面的完整性。
    *   **Smart Interceptor:** 新增 MobileRotate 拦截组件，竖屏访问时显示“终端接入”提示遮罩。
    *   **Transition FX:** 实现从竖屏转横屏时的“系统初始化”过渡动画（带进度条与故障文字效果），增强沉浸感。
    *   **Global Zoom:** 针对移动端横屏实施 transform 全局缩放，配合 125vw 视口补偿，复刻 PC 端布局体验。
*   **💄 Login Terminal 2.0 (登录页进化):**
    *   **Responsive Fix:** 彻底解决移动端软键盘遮挡与内容溢出问题，引入 clamp() 流体排版与弹性滚动机制。
    *   **Visual Polish:** 优化输入框焦点光晕与 Logo 在矮屏下的自适应显示。
*   **🔌 System Interaction (系统交互):**
    *   **Logout Protocol:** 重构退出登录流程，新增悬浮式 "红色警示横幅" 与 "终端关机动画"，替代原生弹窗。
    *   **Sidebar Logic:** 优化侧边栏播放器在折叠/展开状态下的布局表现，修复底部按钮在缩放模式下的截断问题 (flex-shrink: 0)。

### [v0.4.1.0] - Access & Media Patch
> **Time:** 2025-11-23 01:31
*   **🔗 Data Binding & Permission (数据绑定与权限松绑):**
    *   **功能:** 实现普通用户 (Tempop) 与正式干员 (Profile) 的文件上传归属绑定，确保“谁传的谁能看”。
    *   **方法:** 移除数据库 files 表对 profiles 的外键强约束；后端 POST /files/ 接口自动从 Token 解析并绑定 uploader_id；鉴权依赖 (dependencies.py) 升级为支持多表身份查询。
*   **🎵 Secure Media Stream (安全媒体流):**
    *   **功能:** 修复 R2 私有存储桶音频无法播放的问题 (403 Forbidden)。
    *   **方法:** 后端新增 Presigned GET URL 生成逻辑，在返回文件列表时动态将被动地址替换为带签名的临时访问链接。
*   **🎧 Seamless Playback & Auto-Play (无缝播放体验):**
    *   **功能:** 实现登录/注册后 BGM 自动播放，且切换页面不中断。
    *   **方法:**
        *   重构布局 (default.vue) 使用 v-show 替代 v-if 以维持播放器组件活性。
        *   移除登录页阻塞式 alert，确保用户点击事件能直接触发 audio.play()。
        *   优化 SidebarPlayer 组件的 load() 重载机制，解决切歌无声问题。
*   **💄 UI Polish (界面微调):**
    *   **功能:** 优化侧边栏播放器在收起/展开状态下的布局表现。
    *   **方法:**
        *   重写 .mini-player 样式，收起时仅居中显示播放按钮，隐藏文本与光盘图标。
        *   展开时文本区域平滑滑出 (transition: width/opacity)。
        *   侧边栏顶部 Logo 布局下移，增加呼吸感。
*   **⚡ Client-Side Rendering (CSR 优化):**
    *   **功能:** 彻底解决 Wiki 页面刷新时的 401/403 报错与水合不匹配问题。
    *   **方法:** 对鉴权强相关页面 (wiki.vue) 强制禁用 SSR (server: false)，并使用 onRequest 拦截器动态注入 Token。

### [v0.4.0] - Security & Access Control Protocol
> **Time:** 2025-11-22 17:18
* **🔐 Authentication System (鉴权核心):**
    * 实装 **Supabase Auth** 完整流程，支持邮箱/密码登录与注册。
    * 前端集成 `@nuxtjs/supabase` 模块，实现 Session 状态管理与路由守卫 (Route Guard)。
    * 新增 **"断开连接 (Logout)"** 功能，侧边栏底部按钮支持根据登录状态智能切换。
* **🛡️ RBAC & Isolation (权限控制):**
    * **Data Isolation:** 后端 `GET /files/` 接口实装 JWT Token 校验 (`dependencies.py`)，实现“普通干员仅可见自己文件，管理员可见全局”的数据隔离策略。
    * **Tempop Protocol:** 重构数据库触发器，新注册用户自动隔离至 `tempop` (临时人员表)，需管理员审批后方可转入 `profiles` (正式干员表)。
    * **Admin API:** 新增 `routers/admin.py`，提供申请列表查询与人员转正接口。
* **💄 Login Terminal UI (登录终端):**
    * 全新设计的沉浸式登录页面 (`/login`)，移除侧边栏干扰，采用全屏独占模式。
    * **Visual Effects:** 实装 **CSS Mask 物理遮罩** Logo 变色技术，以及基于 SVG Base64 的**噪点粒子渐隐 (Noise Fade)** 动效。
    * **Interaction:** 优化输入框交互 (`box-sizing` 修复) 与错误反馈机制 (自动清洗空格、人性化报错提示)。
    * **Responsive:** 登录卡片与 Logo 针对移动端进行了深度适配，保证多端体验一致。
* **🐛 Stability:**
    * 修复 `wiki.vue` 在开发环境下因数据库冷启动导致的 `signal timed out` 问题 (超时阈值提升至 60s)。
    * 解决前端 `useSupabaseClient` 自动导入失效导致的构建错误 (重置 `package.json` 依赖)。

### [v0.3.2.2] - Mobile UI Polish
> **Time:** 2025-11-22 03:13
* **🐛 UI Hotfix:**
    * **Vertical Stacking:** 强制移动端首页标题与筛选 Tabs 上下分行，修复文本重叠问题。
    * **Touch Target:** 将 Wiki 页面的刷新按钮改为全宽 (Full Width) 布局，避免屏幕边缘截断，并提升触摸体验。
    * **Spacing:** 增加移动端底部 Padding，防止内容被底部导航栏遮挡。

### [v0.3.2.1] - Mobile Terminal Adaptation
> **Time:** 2025-11-22 03:00
* **📱 Responsive Design (移动端适配):**
    * **Navigation:** 实现 **Sidebar (侧边栏)** 到 **Bottom Tab Bar (底部导航)** 的形态切换，释放移动端水平空间。
    * **Dashboard:** 优化首页 **Hero Title** 排版，引入自动换行与字号缩放，修复大屏文字截断问题；资产网格在窄屏下自动切换为单列布局。
    * **Protocol Upload:** 重构上传页布局逻辑，移动端采用 **垂直堆叠 (Vertical Stack)** 模式，彻底修复 PRTS 动画与文字层级重叠、溢出的视觉 Bug。
    * **Archive Wiki:** 优化文件列表项 (`FileListItem`) 的移动端展示，精简元数据列，适配窄屏阅读体验。
* **🔧 UX Polish:** 增加全局 `mobile-only` / `desktop-only` 响应式工具类，统一管理多端显隐逻辑。

### [v0.3.2] - Database Ecosystem & Archive Protocol
> **Time:** 2025-11-22 02:23
* **🗄️ Database Expansion:**
    * 实装 **Supabase (PostgreSQL)** 完整架构，新增 `files` (协议档案), `profiles` (干员档案), `audit_logs` (审计日志), `blueprints` (构建蓝图) 表结构。
    * 优化数据库连接池配置 (`pool_pre_ping`, `keepalives`)，彻底修复 Serverless 环境下的 SSL 解密失败与连接断开问题。
* **📘 Feature: Industrial Wiki:**
    * 上线 **"协议档案库" (Wiki)** 模块，实现 R2 云端文件的可视化列表展示与下载。
    * 后端新增 `GET /files/` 与 `POST /files/` 接口，打通 "上传 -> 录入 -> 展示" 的数据全链路闭环。
* **🎨 Engineering & UI:**
    * **CSS Architecture:** 完成前端样式重构，实现 CSS 与 Vue 组件的完全分离 (`wiki.css`, `component.css`)，提升代码可维护性。
    * **UX Optimization:** 优化上传进度条逻辑，新增 `Processing` (数据库写入) 状态反馈，解决签名阶段进度卡死问题。
* **🐛 Fixes:**
    * 修复本地开发环境 `.env` 加载导致的 R2 连接阻塞问题。
    * 补全路由缺口 (`/editor`, `/settings`)，消除 Vue Router 导航警告。

### [v0.3.1] - Upload Protocol Stabilized
> **Time:** 2025-11-22 01:25
* **✅ Verification:** 完成公网环境 (Zeabur Public Network) 下的**全链路上传测试**，确认前端直传 Cloudflare R2 云端链路稳定。
* **🔧 Hotfix:**
    * 修复容器运行时因 `DATABASE_URL` 环境变量缺失导致的 `pydantic ValidationError` 崩溃循环。
    * 修正 `config.py` 与 `main.py` 的代码结构冲突，恢复中间件 (Middleware) 的正确挂载顺序。
    * 精准配置生产环境 CORS 白名单，彻底解决公网域名下的跨域阻断问题。

### [v0.3.0] - Protocol Transmission Module
> **Time:** 2025-11-21 23:00
*   **☁️ Storage:** 集成 **Cloudflare R2** 对象存储，实现后端预签名 (Presigned URL) 鉴权流程。
*   **📤 Feature:** 新增 **协议上传 (Upload)** 模块，支持文件拖拽与直传云端，绕过后端带宽限制。
*   **✨ UI/UX:**
    *   实装 **PRTS 风格** 动态上传监视器 (SVG + CSS Animation)。
    *   优化状态交互：待机呼吸、上传充能、成功结算动画。
    *   修复 SVG 层级渲染问题，提升视觉锐度与透明质感。

### [v0.2.2] - Global Deployment & Connectivity
> **Time:** 2025-11-21 22:10
*   **🚀 Deployment:** 前后端服务全栈部署至 **Zeabur** (Serverless)，实现公网多端访问。
*   **🌐 Network:** 配置生产环境 CORS 白名单，打通云端前端 (Zeabur Web) 与后端 (Zeabur API) 的通信链路。
*   **🔧 Frontend:** 重构 API 调用逻辑，引入 `runtimeConfig` 实现后端地址的动态切换 (自动识别 Local/Prod 环境)。
*   **📱 Compatibility:** 验证移动端与桌面端响应式布局，工业风 UI 在公网环境下渲染正常。

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