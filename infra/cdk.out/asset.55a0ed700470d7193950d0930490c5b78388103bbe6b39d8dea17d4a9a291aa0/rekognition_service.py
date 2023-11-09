import boto3
from values_objects import FaceImage

class RekognitionService:
    def __init__(self):
        self.rek_client = boto3.client("rekognition")

    def compare_faces(
        self,
        source_image_bytes: FaceImage,
        target_image_bytes: FaceImage,
        similarity_threshold=0.9,
    ):
        return self.rek_client.compare_faces(
            SimilarityThreshold=similarity_threshold,
            SourceImage={"Bytes": source_image_bytes.image_bytes},
            TargetImage={"Bytes": target_image_bytes.image_bytes},
        )
