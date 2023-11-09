from s3_event_entity import S3EventEntity
from rekognition_service import RekognitionService
from values_objects import FaceImage
from rekognition_response_entity import RekognitionResponseFactory, RekognitionResponse
from response_identity_verifier import IdentityVerifierResponse


class IdentityVerifier:
    def __init__(self, rekognition_services: RekognitionService):
        self.rekognition_service = rekognition_services
        self.SIMILARITY_THRESHOLD = 85.0

    def verify_identity(
        self, source_image_bytes: FaceImage, target_image_bytes: FaceImage
    ) -> IdentityVerifierResponse:
        rekognition_response = self.rekognition_service.compare_faces(
            source_image_bytes,
            target_image_bytes,
            similarity_threshold=self.SIMILARITY_THRESHOLD,
        )
        rekognition_response_object: RekognitionResponse = (
            RekognitionResponseFactory.create_from_dict(rekognition_response)
        )

        if rekognition_response_object.face_matches:
            return IdentityVerifierResponse(
                similarity=rekognition_response_object.face_matches[0].similarity,
                reason="Identity verification was successful.",
                confidence=rekognition_response_object.face_matches[0].confidence,
            )
        elif rekognition_response_object.unmatched_faces:
            return IdentityVerifierResponse(
                similarity=0,
                reason="There are no matches",
                confidence=rekognition_response_object.unmatched_faces[0].confidence,
            )
