from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import create_db_and_tables
from routers import assets,upload,files,admin

# --- 生命周期管理 ---
# 在 App 启动前，自动检查并创建数据库表
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan # 挂载生命周期
)

# --- CORS 配置 (保持不变) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 注册路由 ---
# 把 assets 的接口挂载到主程序上
app.include_router(assets.router)
app.include_router(upload.router)
app.include_router(files.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"system": "Endfield Protocol", "status": "Online"}