import boto3
from models import InputRequest
from os import environ,path
from typing import Any,Mapping,Tuple
from json import loads
from logging import Logger
from random import randint
from base64 import b64decode

logger = Logger(name="LambdaFunction")
SIMILARITY_THRESHOLD = 85

rek_client = boto3.client("rekognition")

def handler(event: Mapping[str:Any]):
    print(event)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    