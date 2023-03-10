from app.files import Example


def test_example(s3):
    """Test the example file."""
    example = Example.load(s3.name)
    example.update()
    example.save(s3.name)
    assert "timestamp" in example.mapping
