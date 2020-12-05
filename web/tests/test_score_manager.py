import pytest

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

def test_class_definition():
    """G0001 test class name == ScoreManager"""
    assert type(ScoreManager == ScoreManager)


def test_manager_len(manager, good):
    """G0002 correct length is returned"""
    manager.add_score(good)
    assert len(manager) == 1


def test_add_score(manager):
    """G0003 Incorrect type raises TypeError"""
    with pytest.raises(TypeError):
        manager.add_score("test")


def test_manager_scores_property(manager):
    """G0004 scores is a property"""
    assert type(ScoreManager.scores) == property


def test_manager_scores(manager, good, bad):
    """G0005 Correct value is returned"""
    manager.add_score(bad)
    manager.add_score(good)
    assert manager.scores == [
        {"name": "Good", "score": 999},
        {"name": "Bad", "score": 1},
    ]


def test_manager_remove_scores_user(manager, good):
    """G0006 Correct score is removed"""
    for _ in range(0, 5):
        manager.add_score(good)

    manager.remove_user_score("Good")

    assert len(manager) == 0
