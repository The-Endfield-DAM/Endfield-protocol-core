from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from sqlmodel import Session
from pydantic import BaseModel
from database import get_session
from models import Profile, Tempop
from dependencies import get_current_user
from services.storage import generate_presigned_url

router = APIRouter(
    prefix="/users",
    tags=["User Info (用户信息)"]
)

# 🟢 补全缺失的数据模型定义
class UserUpdate(BaseModel):
    code: str | None = None       # 干员代号
    department: str | None = None # 部门
    avatar_url: str | None = None # 头像链接

@router.get("/me")
def read_users_me(current_user: Union[Profile, Tempop] = Depends(get_current_user)):
    """
    获取当前登录用户的详细档案信息
    """
    
    # 🟢 核心处理：处理头像链接
    # 如果数据库里有值，说明存的是 R2 Key，需要转换成签名 URL
    real_avatar_url = None
    if current_user.avatar_url:
        # 判断一下是否已经是 http 开头（兼容旧数据或外部链接）
        if current_user.avatar_url.startswith("http"):
            real_avatar_url = current_user.avatar_url
        else:
            # 如果不是 http，说明是 Key，生成临时链接
            real_avatar_url = generate_presigned_url(current_user.avatar_url)

    # 情况 A: 正式干员 (Profile)
    if isinstance(current_user, Profile):
        return {
            "id": current_user.id,
            "type": "profile",
            "code": current_user.code,
            "role": current_user.role,
            "department": current_user.department,
            "avatar_url": real_avatar_url, # 🟢 使用处理后的链接
            "status": "active"
        }
        
    # 情况 B: 待审核人员 (Tempop)
    else:
        return {
            "id": current_user.id,
            "type": "tempop",
            "code": current_user.code,
            "email": current_user.email,
            "avatar_url": real_avatar_url, # 🟢 使用处理后的链接
            "status": current_user.status,
            "role": "guest"
        }

@router.patch("/me")
def update_user_me(
    user_update: UserUpdate,
    session: Session = Depends(get_session), # 🟢 现在 get_session 已正确导入
    # 🟢 类型提示涵盖两者
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    """
    更新当前用户的档案信息 (支持正式干员和临时人员)
    """
    
    # 更新字段 (这些字段在 Profile 和 Tempop 表中都存在)
    if user_update.code is not None:
        current_user.code = user_update.code
    
    # 注意：Department 只有 Profile 有，Tempop 没有这个字段，需要判断
    if user_update.department is not None:
        if isinstance(current_user, Profile):
            current_user.department = user_update.department
        else:
             # 如果是 Tempop 尝试修改部门，忽略
             pass

    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url

    try:
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        # 返回时统一转换为字典，避免类型差异问题
        return {"message": "Profile updated", "user": current_user.model_dump()}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))