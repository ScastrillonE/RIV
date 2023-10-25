from models import InputRequest
import boto3
from os import environ, path
from typing import Any, Mapping, Tuple
from json import loads
from logging import Logger
from random import randint
from base64 import b64decode

logger = Logger(name='LambdaFunction')
SIMILARITY_THRESHOLD = 85.0

rek_client = boto3.client('rekognition')

def handler(event:Mapping[str,Any],_=None):
  inputRequest = InputRequest(event)
 
  try:
    response = rek_client.compare_faces(
      SimilarityThreshold=0.9,
      SourceImage={
            'S3Object': {
              'Bucket': inputRequest.bucket,
              'Name': inputRequest.idcard_name
          }
      },
      TargetImage={
          'S3Object': {
              'Bucket': inputRequest.bucket,
              'Name': inputRequest.name
          }
      })

    '''
    Confirm these are approximately the same image.
    '''
    if len(response['FaceMatches']) == 0:
      return { 
        'IsMatch':False,
        'Reason': 'Property $.FaceMatches is empty.'
      }
    facenotMatch = False
    for match in response['FaceMatches']:
      similarity:float = match['Similarity']
      if similarity > SIMILARITY_THRESHOLD:
        print("SUCCESS")
        # return { 
        #   'IsMatch':True,
        #   'Reason': 'All checks passed.'
        # }
      else:
        facenotMatch = True
    if facenotMatch:
        print("NOT MATCH")
    #   return { 
    #       'IsMatch':False,
    #       'Reason': 'Similarity comparison was below threshold (%f < %f).' % (similarity, SIMILARITY_THRESHOLD)
    #   }

    print("END CODE")
    # return { 
    #   'IsMatch':True,
    #   'Reason': 'All checks passed.'
    # }
  except Exception as error:
    print('Comparing({}) to ID Card failed - {}'.format(
      inputRequest.user_id, str(error)))
    raise error
