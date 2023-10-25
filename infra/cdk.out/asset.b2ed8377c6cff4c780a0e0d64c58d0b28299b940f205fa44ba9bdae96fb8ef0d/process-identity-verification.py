import boto3
import logging
from typing import Any, Mapping
from s3_event_entity import S3EventEntity
from rekognition_service import RekognitionService
from identity_verifier import IdentityVerifier
from image_utils import extract_images_from_zip,download_zip_from_s3


logger = logging.getLogger(__name__)
SIMILARITY_THRESHOLD = 85.0


def handler(event: Mapping[str, Any], _=None) -> dict:
    s3_event:S3EventEntity = S3EventEntity.from_event(event)
    
    try:
        zip_bytes = download_zip_from_s3(s3_event=s3_event)
        images_dict = extract_images_from_zip(zip_bytes=zip_bytes)
        
        rekognition_service = RekognitionService()
        identity_verifier = IdentityVerifier(rekognition_services=rekognition_service)
        
        result = identity_verifier.verify_identity(source_image_bytes=images_dict["source"],target_image_bytes=images_dict["target"])
        
        print("REULSTADOOOOOO ",result)

    except Exception as error:
        print('Comparing to ID Card failed - {}'.format(str(error)))
        logger.error('Comparing to ID Card failed - %s', str(error))
        raise error
