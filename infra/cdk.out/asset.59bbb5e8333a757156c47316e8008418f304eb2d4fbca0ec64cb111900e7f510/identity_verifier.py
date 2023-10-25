#identify verifier
from s3_event_entity import S3EventEntity
from rekognition_service import RekognitionService
from values_objects import FaceImage
from rekognition_response_entity import FaceMatch

class IdentityVerifier:
    def __init__(self,rekognition_services:RekognitionService):
        self.rekognition_service = rekognition_services
        self.SIMILARITY_THRESHOLD = 85.0

    def verify_identity(self,source_image_bytes:FaceImage,target_image_bytes:FaceImage) -> dict:
        
        response = self.rekognition_service.compare_faces(source_image_bytes,target_image_bytes,similarity_threshold=self.SIMILARITY_THRESHOLD)
        face_match :FaceMatch = FaceMatch().get_data_from_response_rekognition(response=response)
        if len(response['FaceMatches']) == 0:
            return {
                'IsMatch': False,
                'Reason': 'Property $.FaceMatches is empty.'
            }

        face_not_matched = True
        for match in response['FaceMatches']:
            similarity = match['Similarity']
            if similarity > self.SIMILARITY_THRESHOLD:
                face_not_matched = False
                break

        if face_not_matched:
            return {
                'IsMatch': False,
                'Reason': 'Similarity comparison was below threshold (%f < %f).' % (similarity, self.SIMILARITY_THRESHOLD)
            }

        return {
            'IsMatch': True,
            'Reason': 'All checks passed.'
        }