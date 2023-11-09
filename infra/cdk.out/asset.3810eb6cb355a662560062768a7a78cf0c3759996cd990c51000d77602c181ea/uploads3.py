import json
import boto3
import base64

s3_client = boto3.client('s3')

def handler(event, context):
    request_body = json.loads(event['body'])
    
    zip_file_content_base64 = request_body.get('zip_file', None)
    
    if zip_file_content_base64 is None:
        return {
            'statusCode': 400,
            'body': json.dumps('No se proporcionó un archivo .zip en la solicitud.')
        }

    try:
        
        zip_file_content = base64.b64decode(zip_file_content_base64)

        s3_client.put_object(
            Bucket='rekognition-face-assets',
            Key='archivo.zip',
            Body=zip_file_content
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('El archivo .zip se subió correctamente al bucket de S3.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error al subir el archivo .zip al bucket de S3.')
        }
