import json
import logging
from unittest.mock import patch

import pytest

from app.adapters.common.json_file_handler import read_json_file, write_json_file


def test_read_json_file_returns_empty_list_when_file_does_not_exist(tmp_path):
    assert read_json_file(tmp_path / "non_existent.json") == []


def test_read_json_file_returns_data_on_valid_json(tmp_path):
    file_path = tmp_path / "test.json"
    data = [{"id": "123", "name": "Pasta"}]
    file_path.write_text(json.dumps(data), encoding="utf-8")
    result = read_json_file(file_path)

    assert result == data


def test_read_json_file_returns_empty_list_when_content_is_not_a_list(tmp_path):
    file_path = tmp_path / "object.json"
    file_path.write_text('{"key": "value"}', encoding="utf-8")

    assert read_json_file(file_path) == []


def test_read_json_file_logs_error_and_returns_empty_list_on_corrupt_json(
    tmp_path, caplog
):
    file_path = tmp_path / "corrupt.json"
    file_path.write_text("{corrupt json content", encoding="utf-8")
    with caplog.at_level(logging.ERROR):
        result = read_json_file(file_path)

    assert result == []
    assert "Failed to decode" in caplog.text


def test_read_json_file_logs_error_and_returns_empty_list_on_os_error(tmp_path, caplog):
    file_path = tmp_path / "test.json"
    file_path.write_text("[]", encoding="utf-8")
    with (
        patch("builtins.open", side_effect=OSError("Read failure")),
        caplog.at_level(logging.ERROR),
    ):
        result = read_json_file(file_path)

    assert result == []
    assert "Failed to access" in caplog.text


def test_write_json_file_creates_dir_and_writes_valid_json(tmp_path):
    file_path = tmp_path / "nested" / "dir" / "recipes.json"
    data = [{"id": "123", "title": "Pizza"}]
    write_json_file(file_path, data)

    assert file_path.exists()
    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert content == data


def test_write_json_file_logs_error_and_raises_os_error(tmp_path, caplog):
    file_path = tmp_path / "test.json"
    data = [{"id": "123"}]
    with (
        patch("builtins.open", side_effect=OSError("Disk write error")),
        caplog.at_level(logging.ERROR),
        pytest.raises(OSError, match="Disk write error"),
    ):
        write_json_file(file_path, data)

    assert "Failed to write" in caplog.text
