#image_utils
import zipfile
import base64
import boto3
import os
from  botocore import exceptions
from typing import Dict
from io import BytesIO
from s3_event_entity import S3EventEntity
from values_objects import FaceImage
from errors import S3AccessDeniedError,AWSClientError

def download_zip_from_s3(s3_event:S3EventEntity):
    s3_client = boto3.client('s3')
    try:
        print(s3_event)
        response = s3_client.get_object(Bucket=s3_event.bucketName, Key=s3_event.objectKey)
        return BytesIO(response['Body'].read())
    except exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == "AccessDenied":
            raise S3AccessDeniedError("Access denied error occurred in S3 operation.")
        else:
            # Capturar otros errores de AWS y manejarlos según sea necesario
            raise AWSClientError(f"AWS error occurred: {str(e)}")

def extract_images_from_zip(zip_bytes)->Dict[str,FaceImage]:
    image_dict = {}
    with zipfile.ZipFile(zip_bytes, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            folder_name = os.path.dirname(file_info.filename)
            if file_info.is_dir() == False:
                with zip_ref.open(file_info) as file:
                    file_content = file.read()
                    image_base64 = base64.b64encode(file_content).decode('utf-8')
                    image_dict[folder_name] = FaceImage(image_bytes=image_base64,metadata=file_info)
    return image_dict
