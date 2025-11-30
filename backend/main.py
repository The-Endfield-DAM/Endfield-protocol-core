from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import create_db_and_tables
from routers import assets, upload, files, admin, users, stats, activities

# --- 生命周期管理 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# --- 🔴 核心修复：移除 "*"，严格指定域名 ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3000/login",
    # 如果你有其他的本地开发端口（如 3001），也要加在这里
    "https://endfield-home.zeabur.app"
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# --- CORS 配置 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # 允许携带 Token/Cookie
    allow_methods=["*"],    # 允许所有方法 (GET, POST...)
    allow_headers=["*"],    # 允许所有 Header
)

# --- 注册路由 ---
app.include_router(assets.router)
app.include_router(upload.router)
app.include_router(files.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(stats.router)
app.include_router(activities.router)

@app.get("/")
def read_root():
    return {"system": "Endfield Protocol", "status": "Online"}