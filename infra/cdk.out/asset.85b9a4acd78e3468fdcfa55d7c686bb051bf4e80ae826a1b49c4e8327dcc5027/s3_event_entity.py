from typing import Any, Mapping
from base64 import b64decode


class S3EventEntity:
    def __init__(
        self,
        event_time,
        event_name,
        principal_id,
        request_id,
        response_id,
        bucket_name,
        object_key,
    ):
        self.eventTime = event_time
        self.eventName = event_name
        self.principalId = principal_id
        self.requestId = request_id
        self.xAmzId2 = response_id
        self.bucketName = bucket_name
        self.objectKey = object_key

    @classmethod
    def from_event(cls, data: Mapping[str, Any]) -> "S3EventEntity":
        data = data["Records"][0]
        return cls(
            data["eventTime"],
            data["eventName"],
            data["userIdentity"]["principalId"],
            data["responseElements"]["x-amz-request-id"],
            data["responseElements"]["x-amz-id-2"],
            data["s3"]["bucket"]["name"],
            data["s3"]["object"]["key"],
        )
