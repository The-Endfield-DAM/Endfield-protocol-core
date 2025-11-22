from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select,desc
from database import get_session
from models import File, Profile
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
    current_user: Profile = Depends(get_current_user) # 🔐 强制要求登录
):
    """
    获取文件列表 (已实现权限隔离)
    """
    # 1. 如果是管理员，查看所有文件
    if current_user.role == "admin":
        statement = select(File).order_by(desc(File.created_at))
    
    # 2. 如果是普通干员，只查看自己的文件
    else:
        statement = select(File).where(File.uploader_id == current_user.id).order_by(desc(File.created_at))
        
    results = session.exec(statement).all()
    return results