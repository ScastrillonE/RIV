import json
import boto3
import base64

s3_client = boto3.client("s3")


def handler(event, context):
    request_body = json.loads(event["body"])

    zip_file_content_base64 = request_body.get("zip_file", None)
    zip_file_name = request_body.get("zip_name", None)
    print(zip_file_name)
    if zip_file_content_base64 is None and zip_file_name is None:
        return {
            "statusCode": 400,
            "body": json.dumps(
                "Error: No se proporcionó un archivo ZIP en la solicitud. Asegúrate de incluir tanto el contenido como el nombre del archivo en el formato adecuado."
            ),
        }

    try:
        zip_file_content = base64.b64decode(zip_file_content_base64)

        s3_client.put_object(
            Bucket="rekognition-face-assets", Key=zip_file_name, Body=zip_file_content
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                "El archivo .zip se subió correctamente al bucket de S3."
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error al subir el archivo .zip al bucket de S3."),
        }
