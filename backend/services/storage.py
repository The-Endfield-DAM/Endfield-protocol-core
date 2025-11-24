import boto3
from botocore.config import Config
import uuid
import mimetypes               # 🟢 新增：用于猜测文件类型
from urllib.parse import quote # 🟢 新增：用于文件名 URL 编码
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
    生成上传凭证 (POST)
    """
    print(f"⚡ [DEBUG] Generating presigned url for: {file_name}")
    try:
        unique_name = f"{uuid.uuid4()}-{file_name}"
        object_name = f"uploads/{unique_name}"

        # 3. 向 R2 申请预签名 URL
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

def generate_presigned_url(object_name: str, original_filename: str = None, expiration=3600):
    """
    生成下载/访问链接 (GET)
    🟢 修复中文乱码：如果是文本文件，强制指定 charset=utf-8
    🟢 修复下载体验：强制浏览器弹出下载框，并使用正确的文件名
    """
    try:
        # 1. 猜测文件 MIME 类型
        content_type, _ = mimetypes.guess_type(object_name)
        
        # 2. 构建参数字典
        params = {
            'Bucket': settings.R2_BUCKET_NAME,
            'Key': object_name
        }

        # 3. 修复中文显示乱码
        if content_type and ('text' in content_type or 'json' in content_type):
            params['ResponseContentType'] = f"{content_type}; charset=utf-8"
        
        # 4. 强制下载并指定文件名 (解决浏览器直接打开的问题)
        if original_filename:
            # 对文件名进行 URL 编码
            encoded_name = quote(original_filename)
            # 使用 filename* 语法兼容现代浏览器处理 UTF-8 文件名
            params['ResponseContentDisposition'] = f"attachment; filename*=UTF-8''{encoded_name}"
        else:
            params['ResponseContentDisposition'] = 'attachment'
        
        # 5. 生成带参数的签名链接
        url = s3_client.generate_presigned_url(
            'get_object',
            Params=params,
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"❌ Generate GET URL Failed: {e}")
        return None

def delete_file_from_r2(file_key: str):
    """
    从 R2 物理删除文件
    """
    try:
        s3_client.delete_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=file_key
        )
        return True
    except Exception as e:
        print(f"❌ Delete Object Failed: {e}")
        return False