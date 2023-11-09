class AWSClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class S3AccessDeniedError(AWSClientError):
    def __init__(self, message="Access Denied error occurred in S3 operation."):
        super().__init__(message)

class NoFaceDataException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoFaceMatchException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FaceMatchCreationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)