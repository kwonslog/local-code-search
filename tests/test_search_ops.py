from tools.search_ops import search, fetch

def test_search_and_fetch(sample_dir):
    results = search("readme")
    assert "results" in results
    assert len(results["results"]) >= 1

    file_id = results["results"][0]["id"]
    data = fetch(file_id)
    assert "text" in data
    assert "metadata" in data
