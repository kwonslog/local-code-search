from tools.analyze_ops import analyze_imports, count_lines

def test_analyze_imports(sample_dir):
    result = analyze_imports("example.go")
    assert result["count"] == 2
    assert "fmt" in result["imports"]

def test_count_lines(sample_dir):
    result = count_lines("example.go")
    assert result["total_lines"] > 0
    assert "code_lines" in result
