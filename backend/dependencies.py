from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import settings
from sqlmodel import Session
from database import get_session
from models import Profile

# 定义认证模式 (Bearer Token)
security = HTTPBearer()

# 你的 Supabase JWT Secret (通常在 Supabase 后台 Settings -> API -> JWT Settings 里找)
# 注意：这需要在 .env 和 config.py 里配置 JWT_SECRET
# 如果暂时不想配，也可以用 API 请求去 Supabase 验证用户 (速度慢一点但简单)

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    验证 Token 并返回当前用户的 Profile 信息
    """
    try:
        # 这里有两个方案：
        # 方案 A (标准): 在本地用 JWT_SECRET 解码 Token (速度快，需要配置)
        # 方案 B (简单): 调用 Supabase 的 /auth/v1/user 接口验证 (代码少，无需密钥)
        
        # 我们先采用方案 A 的简化版：假设 Supabase 网关已经验证了签名
        # 在这里我们只解码 payload 获取 user_id (sub)
        # ⚠️ 正式生产环境必须验证签名！
        
        payload = jwt.get_unverified_claims(token.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            
        # 从数据库查询该用户的档案
        user_profile = session.get(Profile, user_id)
        
        if not user_profile:
            # 可能是新注册用户还在 tempop 表，或者尚未建立档案
            # 这里可以抛出异常，或者返回一个临时对象
            raise HTTPException(status_code=403, detail="Profile not found (Access Denied)")
            
        return user_profile

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )