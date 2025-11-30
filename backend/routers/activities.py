from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import File
from datetime import datetime

router = APIRouter(
    prefix="/activities",
    tags=["System Activities"]
)

@router.get("/")
def get_recent_activities(session: Session = Depends(get_session)):
    """获取最近5条活动记录"""
    
    # 查询最新5个文件记录
    recent_files = session.exec(
        select(File)
        .order_by(File.created_at.desc())
        .limit(5)
    ).all()
    
    activities = []
    for file in recent_files:
        # 格式化时间为 HH:MM
        created_time = file.created_at.strftime("%H:%M")
        
        # 判断文件类型
        if file.mime_type and file.mime_type.startswith('audio/'):
            msg = f'Audio track "{file.filename}" uploaded'
        else:
            msg = f'File "{file.filename}" uploaded'
        
        activities.append({
            "time": created_time,
            "type": "upload",
            "message": msg
        })
    
    return activities