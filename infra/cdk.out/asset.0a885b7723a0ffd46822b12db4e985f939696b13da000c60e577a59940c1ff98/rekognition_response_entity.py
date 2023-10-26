class FaceMatch:
    def __init__(self, similarity=None):
        self.similarity = similarity

    def get_data_from_response_rekognition(self,response)->'FaceMatch':
        try:
            similarity = response['FaceMatches'][0]['Similarity']
            return similarity
        except (KeyError, IndexError):
            return None