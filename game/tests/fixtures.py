from views.game_view import GameView
from models.player import Player
from models.maze import Maze
from controllers.game_controller import GameController
from unittest.mock import patch
import pytest


@pytest.fixture
def maze_1():
    return Maze.load_from_file("tests\\models\\test_maze.txt")

@pytest.fixture
def maze_2():
    return Maze.load_from_file("tests\\models\\test_maze_incorrect.txt")

@pytest.fixture
def player_1(maze_1):
    return Player(maze_1)

@pytest.fixture
def game_controller_1(maze_1):
    with patch("builtins.input", side_effect=["A", "B", "C", "D", "E"]):
        return GameController(maze_1)

@pytest.fixture
def game_view_1(player_1, game_controller_1, maze_1):
    with patch("builtins.input", side_effect=["A", "B", "C", "D", "E"]):
        return GameView(player_1, game_controller_1, maze_1.state)