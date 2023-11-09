class IdentityVerifierResponse:
    def __init__(self,similarity,reason,confidence):
        self.similarity = similarity
        self.reason=reason
        self.confidence = confidence