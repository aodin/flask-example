from dataclasses import dataclass
from datetime import datetime
import json
from typing import ClassVar

import boto3


def get_s3():
    return boto3.client("s3")


@dataclass
class Example:
    FILENAME: ClassVar[str] = 'example.json'
    mapping: dict

    @classmethod
    def load(cls, s3_bucket):
        # Missing file will raise botocore.errorfactory.NoSuchKey
        response = get_s3().get_object(Bucket=s3_bucket, Key=cls.FILENAME)
        # The response type is a dict
        # Failed decodes will raise json.decoder.JSONDecodeError
        content = json.loads(response['Body'].read())
        return cls(content)

    def toJSON(self):
        return json.dumps(self.mapping)

    def update(self):
        self.mapping['timestamp'] = datetime.utcnow().timestamp()

    def save(self, s3_bucket):
        """Save the file to S3."""
        get_s3().put_object(
            Bucket=s3_bucket,
            Key=self.FILENAME,
            Body=self.toJSON(),
        )
