from io import BytesIO
import pytest

from scripts import download_sample_data as downloader


class FakeResponse(BytesIO):
    def geturl(self):
        return "https://example.test/sample.csv"


def test_download_saves_file_under_data_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(downloader, "urlopen", lambda *args, **kwargs: FakeResponse(b"a,b\n1,2\n"))
    output = downloader.download_sample(
        "https://example.test/sample.csv", data_dir=tmp_path / "data"
    )
    assert output == tmp_path / "data" / "sample.csv"
    assert output.read_bytes() == b"a,b\n1,2\n"


def test_download_stops_when_size_limit_is_exceeded(monkeypatch, tmp_path):
    monkeypatch.setattr(downloader, "urlopen", lambda *args, **kwargs: FakeResponse(b"too large"))
    data_dir = tmp_path / "data"
    with pytest.raises(ValueError, match="exceeds"):
        downloader.download_sample(
            "https://example.test/sample.csv", max_bytes=4, data_dir=data_dir
        )
    assert list(data_dir.iterdir()) == []


@pytest.mark.parametrize("url", ["http://example.test/file.csv", "not a URL"])
def test_download_requires_https(url, tmp_path):
    with pytest.raises(ValueError, match="HTTPS"):
        downloader.download_sample(url, data_dir=tmp_path)


def test_download_refuses_existing_file_without_force(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    destination = data_dir / "sample.csv"
    destination.write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        downloader.download_sample("https://example.test/sample.csv", data_dir=data_dir)
    assert destination.read_text(encoding="utf-8") == "original"


def test_download_rejects_path_traversal_name(tmp_path):
    with pytest.raises(ValueError, match="simple name"):
        downloader.download_sample(
            "https://example.test/file.csv", filename="../secret", data_dir=tmp_path
        )
