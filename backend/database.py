from sqlmodel import SQLModel, create_engine, Session
from config import settings

# --- 优化连接池配置 ---
# pool_pre_ping=True: 每次从池中拿连接前，先发送一个 "SELECT 1" 探测包。
#   如果连接断了 (SSL error)，它会抛弃这个坏连接，自动重连一个新的。这是解决 SSL 错误的特效药。
# pool_recycle=1800: 每 30 分钟强制回收连接，防止连接在云端因为存活太久被防火墙强行切断。
engine = create_engine(
    settings.DATABASE_URL,
    echo=True, # 生产环境建议改为 False
    pool_pre_ping=True, 
    pool_recycle=1800,
    # 传递给底层 psycopg2 的参数，开启 TCP Keepalive 防止连接假死
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)

def create_db_and_tables():
    # 自动在数据库建表
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session