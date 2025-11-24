from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, desc, col
from database import get_session
from models import File, Profile, Tempop
from dependencies import get_current_user
from services.storage import generate_presigned_url, delete_file_from_r2

router = APIRouter(
    prefix="/files",
    tags=["File Management (文件管理)"]
)

@router.post("/", response_model=File)
def create_file_record(
    file_record: File, 
    session: Session = Depends(get_session),
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    """
    前端上传 R2 成功后，写入数据库
    """
    file_record.uploader_id = current_user.id
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
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    """
    获取文件列表 (带权限隔离 + 自动签名)
    """
    is_admin = isinstance(current_user, Profile) and current_user.role == "admin"

    if is_admin:
        statement = select(File).order_by(desc(File.created_at))
    else:
        statement = select(File).where(File.uploader_id == current_user.id).order_by(desc(File.created_at))
        
    results = session.exec(statement).all()

    for file in results:
        signed_url = generate_presigned_url(file.r2_key, file.filename)
        if signed_url:
            file.url = signed_url
            
    return results

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    session: Session = Depends(get_session),
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    """
    单文件删除
    """
    file_record = session.get(File, file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    is_admin = isinstance(current_user, Profile) and current_user.role == "admin"
    is_owner = file_record.uploader_id == current_user.id
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        delete_file_from_r2(file_record.r2_key)
        session.delete(file_record)
        session.commit()
        return {"message": "File deleted"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 🟢 新增：批量删除接口
@router.post("/batch-delete")
def batch_delete_files(
    file_ids: List[int],
    session: Session = Depends(get_session),
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    """
    批量删除文件 (接收 ID 列表)
    """
    # 1. 查询所有目标文件
    statement = select(File).where(col(File.id).in_(file_ids))
    files = session.exec(statement).all()
    
    if not files:
        return {"message": "No files found", "deleted_count": 0}

    is_admin = isinstance(current_user, Profile) and current_user.role == "admin"
    
    deleted_count = 0
    
    try:
        for file in files:
            # 权限检查：必须是管理员或文件拥有者
            if is_admin or file.uploader_id == current_user.id:
                # 物理删除 R2
                delete_file_from_r2(file.r2_key)
                # 标记数据库删除
                session.delete(file)
                deleted_count += 1
        
        session.commit()
        return {"message": "Batch delete completed", "deleted_count": deleted_count}
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))