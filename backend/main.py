from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- 核心修改：配置跨域中间件 (CORS) ---
# 这是告诉浏览器：“允许来自 localhost:3000 的请求访问我”
origins = [
    "http://localhost:3000",  # 前端开发环境地址
    "http://127.0.0.1:3000",
    # 以后上线了，要把你的域名也加在这里，比如 "https://endfield-protocol.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 允许的来源列表
    allow_credentials=True,     # 允许携带 Cookie
    allow_methods=["*"],        # 允许所有方法 (GET, POST, PUT, DELETE)
    allow_headers=["*"],        # 允许所有请求头
)
# ------------------------------------

@app.get("/")
def read_root():
    return {"message": "Endfield Protocol Backend is Online!"}