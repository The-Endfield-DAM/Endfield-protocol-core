"""
用户信息路由模块

该模块提供用户信息相关的API端点，包括：
- 获取当前用户信息
- 更新当前用户信息

支持两种用户类型：
- Profile: 正式干员
- Tempop: 待审核人员
"""

from typing import Union, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel

from database import get_session
from models import Profile, Tempop
from dependencies import get_current_user
from services.storage import generate_presigned_url


# ==================== 路由器配置 ====================
router = APIRouter(
    prefix="/users",
    tags=["User Info (用户信息)"]
)


# ==================== 数据模型定义 ====================
class UserUpdate(BaseModel):
    code: str | None = None
    department: str | None = None
    avatar_url: str | None = None
    gender: str | None = None
    age: int | None = None
    address: str | None = None
    bio: str | None = None


# ==================== 辅助函数 ====================
def _process_avatar_url(avatar_url: Optional[str]) -> Optional[str]:
    """
    处理头像URL
    
    将存储在数据库中的头像信息转换为可访问的URL：
    - 如果已经是HTTP(S)链接，直接返回（兼容外部链接或旧数据）
    - 如果是存储键值，则生成预签名URL
    
    Args:
        avatar_url: 数据库中存储的头像URL或键值
        
    Returns:
        处理后的可访问URL，若无头像则返回 None
    """
    if not avatar_url:
        return None
    
    # 判断是否已经是完整的URL
    if avatar_url.startswith("http://") or avatar_url.startswith("https://"):
        return avatar_url
    
    # 视为存储键值，生成预签名URL
    return generate_presigned_url(avatar_url)


def _build_profile_response(user: Profile, avatar_url: Optional[str]) -> Dict[str, Any]:
    """
    构建正式干员的响应数据
    
    Args:
        user: Profile 实例
        avatar_url: 处理后的头像URL
        
    Returns:
        包含用户信息的字典
    """
    return {
        "id": user.id,
        "type": "profile",
        "code": user.code,
        "role": user.role,
        "department": user.department,
        "avatar_url": avatar_url,
        "status": "active"
    }


def _build_tempop_response(user: Tempop, avatar_url: Optional[str]) -> Dict[str, Any]:
    """
    构建待审核人员的响应数据
    
    Args:
        user: Tempop 实例
        avatar_url: 处理后的头像URL
        
    Returns:
        包含用户信息的字典
    """
    return {
        "id": user.id,
        "type": "tempop",
        "code": user.code,
        "email": user.email,
        "avatar_url": avatar_url,
        "status": user.status,
        "role": "guest"
    }


def _update_user_fields(
    user: Union[Profile, Tempop],
    user_update: UserUpdate
) -> None:
    """
    更新用户字段
    
    根据用户类型更新相应的字段：
    - code 和 avatar_url: 两种类型均支持
    - department: 仅 Profile 类型支持
    
    Args:
        user: 用户实例（Profile 或 Tempop）
        user_update: 更新数据
    """
    # 更新干员代号
    if user_update.code is not None:
        user.code = user_update.code
    
    # 更新部门（仅对 Profile 有效）
    if user_update.department is not None and isinstance(user, Profile):
        user.department = user_update.department
    
    # 更新头像URL
    if user_update.avatar_url is not None:
        user.avatar_url = user_update.avatar_url


@router.get("/me")
def read_users_me(current_user: Union[Profile, Tempop] = Depends(get_current_user)):
    """
    获取当前登录用户的详细档案信息
    """
    # 处理头像链接 (保持原逻辑)
    real_avatar_url = None
    if current_user.avatar_url:
        if current_user.avatar_url.startswith("http"):
            real_avatar_url = current_user.avatar_url
        else:
            real_avatar_url = generate_presigned_url(current_user.avatar_url)

    # 构建基础信息字典
    user_data = {
        "id": current_user.id,
        "code": current_user.code,
        "email": current_user.email, # 🟢 确保 Profile 也返回 email
        "avatar_url": real_avatar_url,
        # 🟢 新增字段
        "gender": current_user.gender,
        "age": current_user.age,
        "address": current_user.address,
        "bio": current_user.bio,
    }

    # 根据类型补充特定字段
    if isinstance(current_user, Profile):
        user_data.update({
            "type": "profile",
            "role": current_user.role,
            "department": current_user.department,
            "status": "active"
        })
    else:
        user_data.update({
            "type": "tempop",
            "status": current_user.status,
            "role": "guest"
        })
        
    return user_data


@router.patch("/me")
def update_user_me(
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    # 更新通用字段
    if user_update.code is not None:
        current_user.code = user_update.code
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
    
    # 🟢 更新新增字段
    if user_update.gender is not None:
        current_user.gender = user_update.gender
    if user_update.age is not None:
        current_user.age = user_update.age
    if user_update.address is not None:
        current_user.address = user_update.address
    if user_update.bio is not None:
        current_user.bio = user_update.bio

    # 部门只能由 Profile 修改 (或管理员修改，此处仅限制类型)
    if user_update.department is not None:
        if isinstance(current_user, Profile):
            current_user.department = user_update.department
    
    try:
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return {"message": "Profile updated", "user": current_user.model_dump()}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))