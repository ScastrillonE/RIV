from errors import NoFaceDataException,NoFaceMatchException,FaceMatchCreationException

class FaceImage:
    def __init__(self, image_bytes, metadata=None):
        self.image_bytes = image_bytes
        self.metadata = metadata or {}
