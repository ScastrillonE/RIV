from errors import NoFaceDataException,NoFaceMatchException,FaceMatchCreationException

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
            face_matches = response["FaceMatches"]
            if face_matches:
                similarity = face_matches[0]["Similarity"]
                return FaceMatch(similarity)
            else:
                unmatched_faces = response.get("UnmatchedFaces", [])
                if unmatched_faces:
                    raise NoFaceMatchException(
                        "No se encontraron coincidencias de cara en FaceMatches."
                    )
                    return FaceMatch(similarity=0)
                else:
                    raise NoFaceDataException("No hay datos de cara en la respuesta.")
        except (KeyError, IndexError) as e:
            print(f"Error al procesar la respuesta: {e}")
            raise FaceMatchCreationException(
                "Error al crear el objeto FaceMatch desde la respuesta."
            )
