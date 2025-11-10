from tools.meta_ops import get_metadata

def test_metadata(sample_dir):
    result = get_metadata("readme.txt")
    assert "size" in result
    assert result["is_file"] is True
