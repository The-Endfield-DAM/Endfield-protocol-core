from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import settings
from sqlmodel import Session
from database import get_session
from models import Profile, Tempop

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
    验证 Token 并返回当前用户 (可能是 Profile 或 Tempop)
    """
    try:
        payload = jwt.get_unverified_claims(token.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            
        # 🟢 逻辑升级：先查正式干员表
        user = session.get(Profile, user_id)
        
        # 🟢 如果不是正式干员，再查普通干员表 (Tempop)
        if not user:
            user = session.get(Tempop, user_id)

        # 🟢 如果两边都没有，才报错
        if not user:
            raise HTTPException(status_code=403, detail="User not found in database")
            
        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )