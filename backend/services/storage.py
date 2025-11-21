import boto3
from botocore.config import Config
import uuid
from config import settings
import sys

# --- 🕵️‍♂️ 探针 1: 检查配置是否加载 ---
print("--- [DEBUG] Storage Service Initializing ---")
print(f"1. R2_ENDPOINT: {settings.R2_ENDPOINT_URL}")
print(f"2. R2_BUCKET:   {settings.R2_BUCKET_NAME}")
# 只打印前几位，防止泄露
key_sample = settings.R2_ACCESS_KEY_ID[:4] + "***" if settings.R2_ACCESS_KEY_ID else "None"
print(f"3. ACCESS_KEY:  {key_sample}")
print("------------------------------------------")

try:
    # 初始化 S3 客户端
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    print("✅ [DEBUG] Boto3 Client Created Successfully")
except Exception as e:
    print(f"❌ [DEBUG] Boto3 Init Failed: {e}")

def generate_presigned_post(file_name: str, file_type: str):
    """
    生成上传凭证
    """
    print(f"⚡ [DEBUG] Generating presigned url for: {file_name}")
    try:
        unique_name = f"{uuid.uuid4()}-{file_name}"
        object_name = f"uploads/{unique_name}"

        # 3. 向 R2 申请预签名 URL
        # ⚠️ 如果 endpoint 不对，或者网络不通，这里可能会卡住
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.R2_BUCKET_NAME,
                'Key': object_name,
                'ContentType': file_type
            },
            ExpiresIn=3600
        )
        
        print(f"✨ [DEBUG] URL Generated: {presigned_url[:50]}...")

        public_url = f"{settings.R2_ENDPOINT_URL}/{settings.R2_BUCKET_NAME}/{object_name}"

        return {
            "upload_url": presigned_url,
            "file_key": object_name,
            "public_url": public_url
        }

    except Exception as e:
        print(f"❌ [DEBUG] R2 Logic Error: {e}")
        return None