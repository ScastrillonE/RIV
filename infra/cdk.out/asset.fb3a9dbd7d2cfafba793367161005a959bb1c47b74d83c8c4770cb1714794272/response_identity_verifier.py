from json import dumps
from constanst import SIMILARITY_THRESHOLD


class IdentityVerifierResponse:
    def __init__(self, similarity, reason, confidence):
        self.similarity = similarity
        self.reason = reason
        self.confidence = confidence

    @property
    def is_match(self):
        if self.similarity >= SIMILARITY_THRESHOLD and self.confidence >= 97:
            return True
        else:
            return False

    def toJson(self):
        return dumps(self.__dict__.update({'is_match':self.is_match}))
