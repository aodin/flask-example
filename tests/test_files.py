from app.files import Example


def test_example(s3):
    """Test the example file."""
    Example({'timestamp': 0}).save(s3.name)
    example = Example.load(s3.name)
    assert 'timestamp' in example.mapping
