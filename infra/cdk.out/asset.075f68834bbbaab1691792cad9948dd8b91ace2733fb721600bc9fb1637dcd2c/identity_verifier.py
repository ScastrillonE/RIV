from s3_event_entity import S3EventEntity
from rekognition_service import RekognitionService
from values_objects import FaceImage
from rekognition_response_entity import RekognitionResponseFactory, RekognitionResponse
from constanst import SIMILARITY_THRESHOLD


class IdentityVerifier:
    def __init__(self, rekognition_services: RekognitionService):
        self.rekognition_service = rekognition_services

    def verify_identity(
        self, source_image_bytes: FaceImage, target_image_bytes: FaceImage
    ) -> dict:
        rekognition_response = self.rekognition_service.compare_faces(
            source_image_bytes,
            target_image_bytes,
            similarity_threshold=self.SIMILARITY_THRESHOLD,
        )
        print("rekognition_responseeee ", rekognition_response)
        rekognition_response_object: RekognitionResponse = (
            RekognitionResponseFactory.create_from_dict(rekognition_response)
        )
        print(rekognition_response_object.response_metadata)

        if len(rekognition_response["FaceMatches"]) == 0:
            return {"IsMatch": False, "Reason": "Property $.FaceMatches is empty."}

        face_not_matched = True
        for match in rekognition_response["FaceMatches"]:
            similarity = match["Similarity"]
            if similarity > self.SIMILARITY_THRESHOLD:
                face_not_matched = False
                break

        if face_not_matched:
            print("NOT MATCH")
            return {
                "IsMatch": False,
                "Reason": "Similarity comparison was below threshold (%f < %f)."
                % (similarity, self.SIMILARITY_THRESHOLD),
            }

        return {"IsMatch": True, "Reason": "All checks passed."}
