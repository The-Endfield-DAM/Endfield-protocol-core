from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_session
from models import Asset

# 创建一个路由器
router = APIRouter(
    prefix="/assets",
    tags=["Industrial Assets (工业资产)"]
)

# 1. 创建新资产 (POST /assets/)
@router.post("/", response_model=Asset)
def create_asset(asset: Asset, session: Session = Depends(get_session)):
    # 这里的 asset 是前端传来的 JSON 数据
    session.add(asset)
    session.commit()
    session.refresh(asset) # 刷新以获取自动生成的 ID
    return asset

# 2. 获取所有资产 (GET /assets/)
@router.get("/", response_model=List[Asset])
def read_assets(session: Session = Depends(get_session)):
    assets = session.exec(select(Asset)).all()
    return assets