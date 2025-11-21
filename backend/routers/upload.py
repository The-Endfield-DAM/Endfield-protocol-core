from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.storage import generate_presigned_post

router = APIRouter(
    prefix="/upload",
    tags=["File Upload (文件上传)"]
)

# 定义请求模型：前端只需要传这俩参数
class UploadRequest(BaseModel):
    filename: str      # 例如: "reactor_blueprint.glb"
    content_type: str  # 例如: "model/gltf-binary"

@router.post("/presigned")
def get_upload_url(req: UploadRequest):
    """
    获取预签名上传链接 (不经过后端服务器直传 R2)
    """
    result = generate_presigned_post(req.filename, req.content_type)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate upload URL")
    
    return result