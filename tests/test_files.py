import boto3
from moto import mock_s3
import pytest

from app.files import Example


@pytest.fixture(scope='session')
def s3():
    """Mock S3 bucket."""
    with mock_s3():
        conn = boto3.resource('s3', region_name='us-east-1')
        yield conn.create_bucket(Bucket='example')


def test_example(s3):
    """Test the example file."""
    Example({'timestamp': 0}).save(s3.name)
    example = Example.load(s3.name)
    assert 'timestamp' in example.mapping
