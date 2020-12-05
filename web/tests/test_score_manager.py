import io
import pytest
from unittest.mock import patch, mock_open

from score_manager import ScoreManager
from score import Score


@pytest.fixture
def good():
    return Score("Good", 999)


@pytest.fixture
def bad():
    return Score("Bad", 1)


@pytest.fixture
def manager():
    return ScoreManager()


def test_manager_len(manager, good):
    manager.add_score(good)
    assert len(manager) == 1


def test_manager_scores_property(manager):
    assert type(ScoreManager.scores) == property


def test_manager_scores(manager, good, bad):
    manager.add_score(bad)
    manager.add_score(good)
    assert manager.scores == [
        {"name": "Good", "score": 999},
        {"name": "Bad", "score": 1},
    ]


def test_manager_remove_scores_user(manager, good):
    for _ in range(0, 5):
        manager.add_score(good)

    manager.remove_user_score("Good")

    assert len(manager) == 0

def test_manager_serialize(manager, good, bad):
    manager.add_score(good)
    manager.add_score(bad)

    assert manager.serialize() == [good.to_dict(), bad.to_dict()]
