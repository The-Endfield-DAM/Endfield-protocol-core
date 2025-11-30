from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from database import get_session
from models import File, Profile

router = APIRouter(
    prefix="/stats",
    tags=["System Statistics"]
)

@router.get("/")
def get_system_stats(session: Session = Depends(get_session)):
    """获取系统统计数据"""
    
    # 统计文件总数
    file_count = session.exec(select(func.count(File.id))).one()
    
    # 统计音频文件数
    track_count = session.exec(
        select(func.count(File.id))
        .where(File.mime_type.like('audio/%'))
    ).one()
    
    # 统计用户数
    user_count = session.exec(select(func.count(Profile.id))).one()
    
    return {
        "fileCount": file_count,
        "trackCount": track_count,
        "userCount": user_count,
        "systemStatus": "ACTIVE"
    }