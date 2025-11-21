from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 基础信息
    PROJECT_NAME: str = "Endfield Protocol Core"
    VERSION: str = "0.2.0"
    
    # 数据库 (这就强制要求 .env 里必须有 DATABASE_URL，否则报错)
    DATABASE_URL: str
    
    # R2 对象存储
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str = "endfield-assets" # 给个默认值
    R2_ENDPOINT_URL: str

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # 忽略多余的变量 (防止 .env 里有注释导致报错)
        extra = "ignore"

settings = Settings()