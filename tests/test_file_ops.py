from tools.file_ops import read_file, write_file

def test_write_and_read(tmp_path):
    file_path = tmp_path / "sample.txt"
    write_file(str(file_path), "Hello MCP!")
    content = read_file(str(file_path))
    assert content == "Hello MCP!"
