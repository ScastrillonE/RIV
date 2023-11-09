import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'RIVPStack-IdentityVerificationResultsTable95FE563F-12MF5VSPRN325'
table = dynamodb.Table(table_name)

def handler(event, context):
    # Obtiene el ID de la solicitud desde el evento de la solicitud API Gateway
    request_id = event['queryStringParameters']['id']

    try:
        # Realiza una consulta a la tabla de DynamoDB usando el ID
        response = table.get_item(
            Key={
                'RequestId': request_id
            }
        )
        
        item = response.get('Item')

        if item:
            # Devuelve los datos como respuesta si se encontraron en la tabla
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            # Devuelve un error si no se encontraron datos con el ID proporcionado
            return {
                'statusCode': 404,
                'body': 'No se encontraron datos para el ID proporcionado'
            }
    except Exception as e:
        # Devuelve un error si ocurre alguna excepción durante la consulta a la tabla
        return {
            'statusCode': 500,
            'body': f'Error al obtener datos de la tabla: {str(e)}'
        }
