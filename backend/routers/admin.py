from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Tempop, Profile
from uuid import UUID

router = APIRouter(
    prefix="/admin",
    tags=["Admin Protocol (管理员协议)"]
)

# 1. 获取所有申请列表
@router.get("/applications")
def list_applications(session: Session = Depends(get_session)):
    # 实际项目中这里应该加一个 Depends(check_admin_permission)
    return session.exec(select(Tempop).where(Tempop.status == "pending")).all()

# 2. 批准转正 (Promote)
@router.post("/approve/{user_id}")
def approve_operator(user_id: UUID, session: Session = Depends(get_session)):
    # A. 查找临时表记录
    applicant = session.get(Tempop, user_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Application not found")

    # B. 创建正式档案 (Profile)
    official_code = applicant.code.replace("APP", "OP")
    
    new_profile = Profile(
        id=applicant.id,
        code=official_code,
        role="operator", 
        department="新进人员", # 默认部门
        
        # 🟢 核心升级：数据完整迁移
        email=applicant.email,
        avatar_url=applicant.avatar_url,
        gender=applicant.gender,
        age=applicant.age,
        address=applicant.address,
        bio=applicant.bio
    )

    try:
        # C. 事务操作
        session.add(new_profile)
        session.delete(applicant)
        session.commit()
        return {"message": f"Operator {official_code} approved successfully."}
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))