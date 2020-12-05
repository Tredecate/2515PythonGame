import pytest
from score import Score


@pytest.fixture
def bad():
    return Score("Bad", 1)


@pytest.fixture
def good():
    return Score("Good", 999)


def test_score_str(good):
    assert str(good) == "Score: Good (999)"


def test_score_lt(good, bad):
    assert bad < good
    assert not bad > good
