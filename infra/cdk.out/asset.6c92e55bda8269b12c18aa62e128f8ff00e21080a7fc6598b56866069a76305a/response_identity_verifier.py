from json import dumps
from constants import SIMILARITY_THRESHOLD


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
        identity_verifier_response = self.__dict__.copy()
        identity_verifier_response['is_match'] =self.is_match
        return dumps(identity_verifier_response)
