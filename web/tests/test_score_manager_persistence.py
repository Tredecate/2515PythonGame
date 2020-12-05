import io
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from test_score_manager import manager, good, bad

@pytest.fixture
def mock_write():
    class MockReturn:
        def __init__(self, *args, **kwargs):
            self.args = list(args)
            self.kwargs = kwargs
            self.data = io.StringIO()
        def __call__(self, *args, **kwargs):
            self.args.extend(args)
            self.kwargs.update(kwargs)
            return self
        def __enter__(self):
            return self.data
        def __exit__(self, *args, **kwargs):
            pass

    return MockReturn()

def test_manager_to_json(manager, good, bad, mock_write):
    manager.add_score(good)
    manager.add_score(bad)

    with patch('builtins.open', mock_write) as mock_file:
        manager.to_json("test.json")
        assert "test.json" in mock_file.args
        assert mock_file.data.getvalue() == json.dumps({"scores": [{"name": "Good", "score": 999}, {"name": "Bad", "score": 1}]})

def test_manager_from_json(manager):
    JSON_DATA = """{"scores": [{"name": "OTHER", "score": 1}, {"name": "TEST", "score": 100}]}"""
    with patch('builtins.open', mock_open(read_data=JSON_DATA)) as mock_file:
        manager.from_json("test.json")
        assert manager.scores == [
            {"name": "TEST", "score": 100},
            {"name": "OTHER", "score": 1},
        ]

def test_manager_to_csv(manager, good, bad, mock_write):
    manager.add_score(good)
    manager.add_score(bad)
    with patch('builtins.open', mock_write) as mock_file:
        manager.to_csv("test.csv")
        assert "test.csv" in mock_file.args
        assert mock_file.data.getvalue().splitlines() == """name,score\nGood,999\nBad,1\n""".splitlines()


def test_manager_from_csv(manager):
    CSV_DATA = """name,score\nOTHER,1\nTEST,100\n"""

    with patch('builtins.open', mock_open(read_data=CSV_DATA)) as mock_file:
        manager.from_csv("test.csv")
        assert manager.scores == [
            {"name": "TEST", "score": 100},
            {"name": "OTHER", "score": 1},
        ]