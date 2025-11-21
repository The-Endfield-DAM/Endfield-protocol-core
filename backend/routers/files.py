from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select,desc
from database import get_session
from models import File, Profile  # 确保引入了 File 模型

router = APIRouter(
    prefix="/files",
    tags=["File Management (文件管理)"]
)

@router.post("/", response_model=File)
def create_file_record(file_record: File, session: Session = Depends(get_session)):
    """
    前端上传 R2 成功后，调用此接口将文件元数据写入数据库
    """
    # 1. (可选) 这里未来可以验证一下 r2_key 是否真的存在于 R2 中
    
    # 2. 写入数据库
    try:
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
        return file_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.get("/", response_model=List[File])
def read_files(session: Session = Depends(get_session)):
    """
    获取所有已上传的文件档案 (按时间倒序)
    """
    # 按 created_at 倒序排列，最新的在最上面
    statement = select(File).order_by(desc(File.created_at))
    results = session.exec(statement).all()
    return results