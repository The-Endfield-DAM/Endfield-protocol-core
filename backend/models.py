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
    
    # 🟢 新增字段
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    bio: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
    
    # ... (关系定义保持不变)
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
    
    # ... (asset_id, uploader_id 等保持不变) ...
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.id")
    uploader_id: Optional[UUID] = Field(default=None)
    
    filename: str
    r2_key: str
    url: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # 🟢 新增：音乐专属元数据 (默认均为 None，不影响其他文件)
    artist: Optional[str] = None
    cover_r2_key: Optional[str] = None
    lyrics_r2_key: Optional[str] = None

    # ... (Relationships 保持不变) ...
    asset: Optional[Asset] = Relationship(back_populates="files")


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
    avatar_url: Optional[str] = None
    
    # 🟢 新增字段 (与 Profile 保持一致)
    gender: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    bio: Optional[str] = None
    
    status: str = Field(default="pending")
    applied_at: datetime = Field(default_factory=datetime.now)