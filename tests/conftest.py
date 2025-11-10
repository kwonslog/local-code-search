import pytest
from pathlib import Path
from config import BASE_DIR

@pytest.fixture(scope="session")
def sample_dir(tmp_path_factory):
    """테스트용 임시 디렉토리 생성"""
    tmp_dir = tmp_path_factory.mktemp("workspace")
    (tmp_dir / "example.go").write_text('package main\nimport "fmt"\nimport "myapp/internal"\nfunc main(){}')
    (tmp_dir / "readme.txt").write_text("This is a test file.")
    return tmp_dir

@pytest.fixture(autouse=True)
def patch_basedir(monkeypatch, sample_dir):
    """BASE_DIR을 테스트용 디렉토리로 교체"""
    from config import BASE_DIR as real_base
    monkeypatch.setattr("config.BASE_DIR", sample_dir)
    monkeypatch.setattr("utils.security.BASE_DIR", sample_dir)
    yield
    monkeypatch.setattr("config.BASE_DIR", real_base)
    monkeypatch.setattr("utils.security.BASE_DIR", real_base)
