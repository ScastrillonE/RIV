from models import S3EventEntity
import boto3
import logging
from typing import Any, Mapping

logger = logging.getLogger(__name__)
SIMILARITY_THRESHOLD = 85.0

rek_client = boto3.client('rekognition')

def handler(event: Mapping[str, Any], _=None) -> dict:
    print("EVENTTTT ", event)
    input_request:S3EventEntity = S3EventEntity.from_dict(event)
    try:
        response = rek_client.compare_faces(
            SimilarityThreshold=0.9,
            SourceImage={
                'S3Object': {
                    'Bucket': input_request.bucket,
                    'Name': input_request.name
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': input_request.target_bucket,  
                    'Name': input_request.target_name 
                }
            }
        )

        if len(response['FaceMatches']) == 0:
            return {
                'IsMatch': False,
                'Reason': 'Property $.FaceMatches is empty.'
            }

        face_not_matched = True
        for match in response['FaceMatches']:
            similarity = match['Similarity']
            if similarity > SIMILARITY_THRESHOLD:
                print("SUCCESS")
                face_not_matched = False
                break

        if face_not_matched:
            print("NOT MATCH")
            return {
                'IsMatch': False,
                'Reason': 'Similarity comparison was below threshold (%f < %f).' % (similarity, SIMILARITY_THRESHOLD)
            }

        print("END CODE")
        return {
            'IsMatch': True,
            'Reason': 'All checks passed.'
        }
    except Exception as error:
        print('Comparing to ID Card failed - {}'.format(str(error)))
        logger.error('Comparing to ID Card failed - %s', str(error))
        raise error
