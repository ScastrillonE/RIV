class FaceImage:
    def __init__(self, image_bytes, metadata=None):
        self.image_bytes = image_bytes
        self.metadata = metadata or {}


class FaceMatch:
    def __init__(self, similarity: float = 0) -> None:
        self.similarity = similarity


class FaceMatchFactory:
    @staticmethod
    def create_from_response(response) -> FaceMatch:
        try:
            similarity = response["FaceMatches"][0]["Similarity"]
            return FaceMatch(similarity)
        except (KeyError, IndexError):
            print("No se encontró la similitud en los datos proporcionados.")
            return None
