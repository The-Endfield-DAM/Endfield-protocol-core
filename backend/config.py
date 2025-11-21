from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 1. 定义你需要的所有全局变量
    PROJECT_NAME: str = "Endfield Protocol Core"
    VERSION: str = "1.0.0"
    
    # 3. 允许跨域的白名单 (CORS)
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    # 4. 配置读取规则
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# ---------------------------------------------------------
# ⚠️ 报错就是因为缺了下面这一行！
# 我们必须把类实例化成对象，导出的必须是这个 'settings' 变量
# ---------------------------------------------------------
settings = Settings()