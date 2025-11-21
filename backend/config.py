from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 基础信息
    PROJECT_NAME: str = "Endfield Protocol Core"
    VERSION: str = "0.2.0"
    
    # 数据库
    DATABASE_URL: str
    
    # R2 对象存储
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str = "endfield-assets"
    R2_ENDPOINT_URL: str

    # --- 🔴 重点修改这里 ---
    # CORS: 添加你的 Zeabur 前端域名
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://endfield-home.zeabur.app"  # <--- 新增这一行，注意不要带末尾的斜杠 /
    ]
    # ---------------------

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()