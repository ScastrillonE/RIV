from json import dumps
class IdentityVerifierResponse:
    def __init__(self,similarity,reason,confidence):
        self.similarity = similarity
        self.reason=reason
        self.confidence = confidence

    def toJson(self):
        return dumps(self.__dict__)