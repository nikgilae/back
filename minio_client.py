import aiobotocore.session

MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "avatars"


def get_minio_session():
    return aiobotocore.session.get_session()


async def upload_file(file_bytes: bytes, filename: str) -> str:
    session = get_minio_session()
    async with session.create_client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    ) as client:
        try:
            await client.create_bucket(Bucket=BUCKET_NAME)
        except Exception:
            pass

        await client.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=file_bytes,
        )

        return f"{MINIO_ENDPOINT}/{BUCKET_NAME}/{filename}"


async def check_minio() -> bool:
    try:
        session = get_minio_session()
        async with session.create_client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        ) as client:
            await client.list_buckets()
            return True
    except Exception:
        return False