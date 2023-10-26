
from constructs import Construct

from aws_cdk.aws_lambda import Function, Runtime, Code
import aws_cdk.aws_lambda_event_sources as eventsources

from aws_cdk import (
  aws_s3 as s3,
  Stack,
  aws_iam as iam
)

class RIVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, "rekognition-face-assets", bucket_name="rekognition-face-assets")
        
        lambda_role_read_s3 = iam.Role(
            self,
            "LambdaReadS3",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"),
            ],
        )
        
        process_identity_verification_lambda = Function(
            self,
            "process-identity-verification",
            runtime=Runtime.PYTHON_3_8,
            code=Code.from_asset("../lambda/process-identity-verification"),
            handler="process-identity-verification.handler",
            role=lambda_role_read_s3,
        )
        
        process_identity_verification_lambda.add_event_source(eventsources.S3EventSource(bucket,
            events=[s3.EventType.OBJECT_CREATED],
            filters=[s3.NotificationKeyFilter(suffix=".zip")]
            
        ))
        