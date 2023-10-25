#identify verifier
from s3_event_entity import S3EventEntity
from rekognition_service import RekognitionService
from values_objects import FaceImage

class IdentityVerifier:
    def __init__(self,rekognition_services:RekognitionService):
        self.rekognition_service = rekognition_services
        self.SIMILARITY_THRESHOLD = 85.0

    def verify_identity(self,source_image_bytes:FaceImage,target_image_bytes:FaceImage) -> dict:
        
        response = self.rekognition_service.compare_faces(source_image_bytes,target_image_bytes,similarity_threshold=self.SIMILARITY_THRESHOLD)
        if len(response['FaceMatches']) == 0:
            return {
                'IsMatch': False,
                'Reason': 'Property $.FaceMatches is empty.'
            }

        face_not_matched = True
        for match in response['FaceMatches']:
            similarity = match['Similarity']
            if similarity > self.SIMILARITY_THRESHOLD:
                print("SUCCESS")
                face_not_matched = False
                break

        if face_not_matched:
            print("NOT MATCH")
            return {
                'IsMatch': False,
                'Reason': 'Similarity comparison was below threshold (%f < %f).' % (similarity, self.SIMILARITY_THRESHOLD)
            }

        print("END CODE")
        return {
            'IsMatch': True,
            'Reason': 'All checks passed.'
        }