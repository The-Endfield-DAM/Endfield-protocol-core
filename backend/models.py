from typing import Optional
from sqlmodel import Field, SQLModel

# 这是一个数据模型，既是 Pydantic 校验模型，也是数据库表结构
class Asset(SQLModel, table=True):
    # table=True 表示这会在数据库里建一张表
    id: Optional[int] = Field(default=None, primary_key=True)
    
    name: str = Field(index=True)          # 设备名称 (如: 源石反应堆-01)
    code: str = Field(unique=True)         # 设备编号 (如: END-RCT-001)
    type: str                              # 类型 (如: Reactor, Conveyor)
    status: str = Field(default="active")  # 状态 (active, offline, maintenance)
    location: Optional[str] = None         # 坐标/区域