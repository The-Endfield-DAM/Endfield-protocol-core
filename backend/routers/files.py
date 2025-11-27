from typing import List, Union, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
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
    current_user: Union[Profile, Tempop] = Depends(get_current_user),
    # 🟢 新增：支持按 MIME 类型前缀过滤 (例如传 'audio/' 只查音频)
    mime_type_prefix: Optional[str] = Query(None, description="Filter files by MIME type prefix")
):
    """
    获取文件列表 (支持权限隔离 + 类型筛选 + 自动签名)
    """
    # 1. 基础查询
    statement = select(File)

    # 2. 权限过滤
    is_admin = isinstance(current_user, Profile) and current_user.role == "admin"
    if not is_admin:
        # 普通用户只能看自己的
        statement = statement.where(File.uploader_id == current_user.id)
    
    # 🟢 3. 类型过滤 (核心新增)
    if mime_type_prefix:
        statement = statement.where(File.mime_type.startswith(mime_type_prefix))

    # 4. 排序
    statement = statement.order_by(desc(File.created_at))
        
    results = session.exec(statement).all()

    # 5. 动态生成 URL
    for file in results:
        # 签名主文件
        signed_url = generate_presigned_url(file.r2_key, file.filename)
        if signed_url:
            file.url = signed_url
        
        # 🟢 新增：签名封面图
        if file.cover_r2_key:
            signed_cover = generate_presigned_url(file.cover_r2_key)
            if signed_cover:
                file.cover_r2_key = signed_cover # 暂时把 URL 塞回 key 字段传给前端
        
        # 🟢 新增：签名歌词文件
        if file.lyrics_r2_key:
            signed_lyric = generate_presigned_url(file.lyrics_r2_key)
            if signed_lyric:
                file.lyrics_r2_key = signed_lyric

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

@router.post("/batch-delete")
def batch_delete_files(
    file_ids: List[int],
    session: Session = Depends(get_session),
    current_user: Union[Profile, Tempop] = Depends(get_current_user)
):
    """
    批量删除文件
    """
    statement = select(File).where(col(File.id).in_(file_ids))
    files = session.exec(statement).all()
    
    if not files:
        return {"message": "No files found", "deleted_count": 0}

    is_admin = isinstance(current_user, Profile) and current_user.role == "admin"
    
    deleted_count = 0
    
    try:
        for file in files:
            if is_admin or file.uploader_id == current_user.id:
                delete_file_from_r2(file.r2_key)
                session.delete(file)
                deleted_count += 1
        
        session.commit()
        return {"message": "Batch delete completed", "deleted_count": deleted_count}
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))