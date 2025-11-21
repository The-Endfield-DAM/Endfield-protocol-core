import boto3
from botocore.config import Config
import uuid
from config import settings

# 1. 初始化 S3 客户端 (连接 R2)
# R2 完美兼容 S3 协议，所以我们用 boto3 库
s3_client = boto3.client(
    's3',
    endpoint_url=settings.R2_ENDPOINT_URL,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4'),
    region_name='auto' # R2 不区分区域，填 auto 即可
)

def generate_presigned_post(file_name: str, file_type: str):
    """
    生成上传凭证
    :param file_name: 原始文件名 (如 'design.png')
    :param file_type: 文件类型 (如 'image/png')
    """
    try:
        # 2. 生成唯一文件名 (防止用户上传同名文件覆盖)
        # 结果类似: uploads/a1b2c3d4-design.png
        unique_name = f"{uuid.uuid4()}-{file_name}"
        object_name = f"uploads/{unique_name}"

        # 3. 向 R2 申请预签名 URL (有效期 1 小时)
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.R2_BUCKET_NAME,
                'Key': object_name,
                'ContentType': file_type
            },
            ExpiresIn=3600
        )

        # 4. 拼接最终可访问的公开链接
        # 注意：如果没有绑定自定义域名，这里暂时用 R2 的公共测试域名或 Worker 域名
        # 现阶段我们先返回 Object Key，以后再配合 Public Domain
        public_url = f"{settings.R2_ENDPOINT_URL}/{settings.R2_BUCKET_NAME}/{object_name}"

        return {
            "upload_url": presigned_url, # 前端往这里 PUT 文件
            "file_key": object_name,     # 存数据库用的 Key
            "public_url": public_url     # 下载/预览用的 URL
        }

    except Exception as e:
        print(f"❌ R2 Error: {e}")
        return None