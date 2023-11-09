class Face:
    def __init__(self, confidence):
        self.confidence = confidence

class FaceMatch(Face):
    def __init__(self,confidence,similarity):
        super().__init__(confidence)
        self.similarity=similarity

class FaceUnMatch(Face):
    def __init__(self,confidence):
        super().__init__(confidence)


class RekognitionResponse:
    def __init__(self, face_matches:FaceMatch, unmatched_faces:FaceUnMatch, response_metadata):
        self.face_matches = face_matches
        self.unmatched_faces = unmatched_faces
        self.response_metadata = response_metadata


class RekognitionResponseFactory:
    @staticmethod
    def create_from_dict(response_data) -> RekognitionResponse:
        face_matches_data = response_data.get("face_matches", [])
        unmatched_faces_data = response_data.get("unmatched_faces", [])
        response_metadata = response_data.get("response_metadata", {})

        face_matches = [FaceMatch(**match["Face"]) for match in face_matches_data]
        unmatched_faces = [FaceUnMatch(**face) for face in unmatched_faces_data]

        return RekognitionResponse(face_matches, unmatched_faces, response_metadata)
