from constructs import Construct

from aws_cdk.aws_lambda import Function, Runtime, Code
import aws_cdk.aws_lambda_event_sources as eventsources

from aws_cdk import (
    aws_s3 as s3,
    Stack,
    aws_iam as iam,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    Duration,
)


class RIVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(
            self, "rekognition-face-assets", bucket_name="rekognition-face-assets"
        )

        lambda_role = iam.Role(
            self,
            "LambdaReadS3",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
            ],
        )

        process_identity_verification_lambda = Function(
            self,
            "process-identity-verification-lambda",
            runtime=Runtime.PYTHON_3_8,
            code=Code.from_asset("../lambda/process-identity-verification"),
            handler="process-identity-verification.handler",
            role=lambda_role,
            timeout=Duration.minutes(3),
        )
        
        upload_s3_lambda = Function(
            self,
            "upload-s3-lambda",
            runtime=Runtime.PYTHON_3_8,
            code=Code.from_asset("../lambda/uploadS3"),
            handler="uploads3.handler",
            role=lambda_role,
            timeout=Duration.minutes(3),
        )
        
        get_data_lambda = Function(
            self,
            "get-info-dentity-verification-lambda",
            runtime=Runtime.PYTHON_3_8,
            code=Code.from_asset("../lambda/get-info-dentity-verification"),
            handler="get-info-dentity-verification.handler",
            role=lambda_role,
            timeout=Duration.minutes(3),
        )

        generate_pdf_result = Function(
            self,
            "generate-pdf-result-process",
            runtime=Runtime.PYTHON_3_8,
            code=Code.from_asset("../lambda/generate-pdf-result-process")
            handler="generate-pdf-result-process.handler",
            role=lambda_role,
            timeout=Duration.minutes(5)
        )


        process_identity_verification_lambda.add_event_source(
            eventsources.S3EventSource(
                bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[s3.NotificationKeyFilter(suffix=".zip")],
            )
        )


        api = apigateway.RestApi(self, "FileUploadApi")

        integration = apigateway.LambdaIntegration(upload_s3_lambda)
        
        api.root.add_resource("upload").add_method("POST", integration, api_key_required=True)
        # Integración para el endpoint GET
        get_integration = apigateway.LambdaIntegration(get_data_lambda)

        # Crea un recurso para manejar solicitudes con un ID específico
        data_resource = api.root.add_resource("getIdentitySimilarity")
        data_resource.add_method("GET", get_integration, api_key_required=True)
        
        dynamodb_table = dynamodb.Table(
            self, "IdentityVerificationResultsTable",
            partition_key=dynamodb.Attribute(
                name="RequestId",
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.RETAIN 
        )

        # Asocia un permiso de escritura para process_identity_verification_lambda a la tabla
        dynamodb_table.grant_full_access(process_identity_verification_lambda)