from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select,desc
from database import get_session
from models import File, Profile, Tempop
from dependencies import get_current_user

router = APIRouter(
    prefix="/files",
    tags=["File Management (文件管理)"]
)

@router.post("/", response_model=File)
def create_file_record(
    file_record: File, 
    session: Session = Depends(get_session),
    current_user: Profile = Depends(get_current_user) # 🟢 新增：强制要求登录，并获取当前用户
):
    """
    前端上传 R2 成功后，调用此接口将文件元数据写入数据库
    """
    # 1. (可选) 这里未来可以验证一下 r2_key 是否真的存在于 R2 中

    file_record.uploader_id = current_user.id  # 关联上传用户 
    
    # 2. 写入数据库
    try:
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
        return file_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.get("/", response_model=List[File])
def read_files(
    session: Session = Depends(get_session),
    # 🟢 current_user 可能是 Profile 也可能是 Tempop
    current_user: Union[Profile, Tempop] = Depends(get_current_user) 
):
    """
    获取文件列表 (权限分级：管理员看所有，普通用户看自己)
    """
    
    # 1. 检查是否是管理员 (只有 Profile 表里才有 role 字段)
    is_admin = False
    if isinstance(current_user, Profile) and current_user.role == "admin":
        is_admin = True

    # 2. 分级查询
    if is_admin:
        # 管理员：上帝视角
        statement = select(File).order_by(desc(File.created_at))
    else:
        # 普通用户 (Tempop 或 普通Profile)：只能看自己的
        statement = select(File).where(File.uploader_id == current_user.id).order_by(desc(File.created_at))
        
    results = session.exec(statement).all()
    return results