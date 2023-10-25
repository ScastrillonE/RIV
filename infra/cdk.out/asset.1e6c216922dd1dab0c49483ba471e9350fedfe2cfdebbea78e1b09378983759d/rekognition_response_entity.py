class FaceMatch:
    def __init__(self, similarity=None):
        self.similarity = similarity

    def get_data_from_response_rekognition(self,response):
        try:
            similarity = response['FaceMatches'][0]['Similarity']
            return similarity
        except (KeyError, IndexError):
            print("No se encontró la similitud en los datos proporcionados.")
            return None