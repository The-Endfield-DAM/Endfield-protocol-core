from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship, Column, JSON

# --- 1. 干员档案 (Profile) ---
class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: UUID = Field(primary_key=True)
    code: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = Field(default="operator")
    department: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # 关联关系
    # 🔴 核心修复：注释掉 files 关联，因为 File 表的外键已经移除了
    # files: List["File"] = Relationship(back_populates="uploader")
    
    blueprints: List["Blueprint"] = Relationship(back_populates="creator")
    logs: List["AuditLog"] = Relationship(back_populates="operator")


# --- 2. 工业资产 (Asset) ---
class Asset(SQLModel, table=True):
    __tablename__ = "asset" 

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(unique=True)
    type: str
    status: str = Field(default="active")
    location: Optional[str] = None
    
    # 资产依然可以关联文件
    files: List["File"] = Relationship(back_populates="asset")


# --- 3. 协议文件 (File) ---
class File(SQLModel, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")
    
    # 🟢 这里的 foreign_key 已经移除，允许存储 Tempop ID
    uploader_id: Optional[UUID] = Field(default=None) 
    
    filename: str
    r2_key: str
    url: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # 关联对象
    asset: Optional[Asset] = Relationship(back_populates="files")
    # 🟢 这里的反向关联也已移除
    # uploader: Optional[Profile] = Relationship(back_populates="files")


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
    
    data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    creator: Optional[Profile] = Relationship(back_populates="blueprints")


# --- 6. 临时人员 (Tempop) ---
class Tempop(SQLModel, table=True):
    __tablename__ = "tempop"

    id: UUID = Field(primary_key=True)
    email: Optional[str] = None
    code: str
    status: str = Field(default="pending")
    applied_at: datetime = Field(default_factory=datetime.now)