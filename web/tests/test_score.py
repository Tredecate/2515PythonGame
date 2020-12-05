import pytest
from score import Score


@pytest.fixture
def bad():
    return Score("Bad", 1)


@pytest.fixture
def good():
    return Score("Good", 999)

def test_class_definition():
    """F0001 test class name == Score"""
    assert type(Score == Score)


def test_parameter_validation():
    """F0002 Invalid parameters raise ValueError"""
    with pytest.raises(ValueError):
        Score(None, None)
    with pytest.raises(ValueError):
        Score("test", None) 
    with pytest.raises(ValueError):
        Score("test", "test")
    with pytest.raises(ValueError):
        Score(0, 100)
    with pytest.raises(ValueError):
        Score(None, 100)   


def test_score_str(good):
    """F0003 Correct string is returned"""
    assert str(good) == "Score: Good (999)"


def test_score_lt_type(good):
    """F0004 Incorrect type raises TypeError"""
    with pytest.raises(TypeError):
        good < "test"


def test_score_lt(good, bad):
    """F0005 Correct Boolean is returned"""
    assert bad < good
    assert not bad > good
