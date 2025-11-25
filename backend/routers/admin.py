from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from database import get_session
from models import Tempop, Profile
from uuid import UUID
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["Admin Protocol (管理员协议)"]
)

# 1. 获取申请列表 (支持分页)
@router.get("/applications")
def list_applications(
    page: int = Query(1, ge=1), 
    size: int = Query(10, ge=1, le=50), # 默认 10 条一页
    session: Session = Depends(get_session)
):
    # 计算偏移量
    offset = (page - 1) * size
    
    # 查询总数
    total_statement = select(func.count()).where(Tempop.status == "pending").select_from(Tempop)
    total = session.exec(total_statement).one()
    
    # 查询当前页数据
    statement = select(Tempop).where(Tempop.status == "pending").offset(offset).limit(size)
    results = session.exec(statement).all()
    
    return {
        "items": results,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

# 2. 批准转正 (Promote)
@router.post("/approve/{user_id}")
def approve_operator(user_id: UUID, session: Session = Depends(get_session)):
    # A. 查找临时表记录
    applicant = session.get(Tempop, user_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Application not found")

    # B. 创建正式档案 (Profile)
    # 将 APP-xxxx 升级为 OP-xxxx
    official_code = applicant.code.replace("APP", "OP")
    
    new_profile = Profile(
        id=applicant.id,
        code=official_code,
        role="admin", 
        department="基建工程部",
        email=applicant.email,
        avatar_url=applicant.avatar_url,
        gender=applicant.gender,
        age=applicant.age,
        address=applicant.address,
        bio=applicant.bio
    )

    try:
        # C. 事务操作：写入 Profile -> 删除 Tempop -> 提交
        session.add(new_profile)
        session.delete(applicant) 
        session.commit()
        return {"message": f"Operator {official_code} approved successfully."}
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))