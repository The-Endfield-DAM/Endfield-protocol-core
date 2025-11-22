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
    # 生成正式干员代号 (把 APP-xxxx 变成 OP-xxxx)
    official_code = applicant.code.replace("APP", "OP")
    
    new_profile = Profile(
        id=applicant.id,
        code=official_code,
        role="operator", # 默认为普通干员，你也可以改成 admin
        department="新进人员",
        avatar_url="https://ui-avatars.com/api/?name=OP&background=random"
    )

    try:
        # C. 事务操作：写入 Profile -> 删除 Tempop -> 提交
        session.add(new_profile)
        session.delete(applicant) # 从临时表移除
        session.commit()
        return {"message": f"Operator {official_code} approved successfully."}
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))