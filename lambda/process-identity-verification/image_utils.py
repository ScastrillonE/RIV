# image_utils
import zipfile
import base64
import boto3
import os
from botocore import exceptions
from typing import Dict
from io import BytesIO
from s3_event_entity import S3EventEntity
from values_objects import FaceImage
from errors import S3AccessDeniedError, AWSClientError


def download_zip_from_s3(s3_event: S3EventEntity) -> BytesIO:
    s3_client = boto3.client("s3")
    try:
        response = s3_client.get_object(
            Bucket=s3_event.bucketName, Key=s3_event.objectKey
        )
        return BytesIO(response["Body"].read())
    except exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == "AccessDenied":
            raise S3AccessDeniedError("Access denied error occurred in S3 operation.")
        else:
            # Capturar otros errores de AWS y manejarlos según sea necesario
            raise AWSClientError(f"AWS error occurred: {str(e)}")


def extract_images_from_zip(zip_bytes) -> Dict[str, FaceImage]:
    image_dict = {}
    with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
        for file_info in zip_ref.infolist():
            folder_name = os.path.dirname(file_info.filename)
            if file_info.is_dir() == False:
                with zip_ref.open(file_info) as file:
                    file_content = file.read()
                    if len(file_content) <= 4 * 1024 * 1024:  # 4 MB en bytes
                        image_dict[folder_name] = FaceImage(
                            image_bytes=file_content, metadata=file_info
                        )
                    else:
                        pass  # Implementar funcion para reducir peso de las imagenes
    return image_dict
