from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship, Column, JSON

# --- 1. 干员档案 (Profile) ---
class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: UUID = Field(primary_key=True) # 对应 Supabase Auth User ID
    code: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = Field(default="operator")
    department: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # 关联关系 (反向查询用)
    files: List["File"] = Relationship(back_populates="uploader")
    blueprints: List["Blueprint"] = Relationship(back_populates="creator")
    logs: List["AuditLog"] = Relationship(back_populates="operator")


# --- 2. 工业资产 (Asset) - 现有表 ---
class Asset(SQLModel, table=True):
    # 注意：你数据库里表名是 "asset" (单数)，保持一致
    __tablename__ = "asset" 

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(unique=True)
    type: str
    status: str = Field(default="active")
    location: Optional[str] = None
    
    # 新增关联：一个资产可以包含多个文件
    files: List["File"] = Relationship(back_populates="asset")


# --- 3. 协议文件 (File) ---
class File(SQLModel, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 外键关联
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")
    uploader_id: Optional[UUID] = Field(default=None, foreign_key="profiles.id")
    
    filename: str
    r2_key: str      # R2 中的唯一键
    url: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # 关联对象
    asset: Optional[Asset] = Relationship(back_populates="files")
    uploader: Optional[Profile] = Relationship(back_populates="files")


# --- 4. 审计日志 (AuditLog) ---
class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    operator_id: Optional[UUID] = Field(default=None, foreign_key="profiles.id")
    
    action: str
    target: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    operator: Optional[Profile] = Relationship(back_populates="logs")


# --- 5. 构建蓝图 (Blueprint) ---
class Blueprint(SQLModel, table=True):
    __tablename__ = "blueprints"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: Optional[UUID] = Field(default=None, foreign_key="profiles.id")
    
    name: str
    version: str = Field(default="v1.0")
    is_public: bool = Field(default=False)
    
    # 存储复杂的 JSON 数据 (Supabase/PG 特有的 JSONB)
    data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    creator: Optional[Profile] = Relationship(back_populates="blueprints")