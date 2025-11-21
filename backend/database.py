from sqlmodel import SQLModel, create_engine, Session
from config import settings

# --- 核心修改：从 SQLite 切换到 PostgreSQL ---
# echo=True 会打印 SQL 语句，方便调试，生产环境可以改为 False
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    # 这行代码会自动连接 Supabase，并在云端创建你的 Asset 表
    # 如果表已经存在，它会跳过
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session