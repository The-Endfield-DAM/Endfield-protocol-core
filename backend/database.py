from sqlmodel import SQLModel, create_engine, Session
from config import settings # 导入我们之前写的配置

# 1. 定义数据库 URL
# 如果是开发环境，就用本地的 sqlite 文件
# check_same_thread=False 是 SQLite 专用的配置，防止多线程报错
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. 创建引擎
engine = create_engine(sqlite_url, echo=True) # echo=True 会在控制台打印 SQL 语句，方便调试

# 3. 初始化数据库 (自动建表)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. 依赖注入函数 (给 API 用)
# 每次请求进来，给它一个数据库会话；请求结束，自动关闭会话
def get_session():
    with Session(engine) as session:
        yield session