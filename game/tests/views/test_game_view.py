from views.game_view import GameView
from tests.fixtures import *


def test_class_definition(game_view_1):
    """C0001 test class name == GameView"""
    assert type(game_view_1) == GameView

def test_map_render_return(game_view_1, maze_1):
    """C0002 game display text correctly includes a player object"""
    assert "☻" in game_view_1._get_map_display(maze_1.state)

def test_game_over_render_return(game_view_1, game_controller_1):
    """C0003 game over display text correctly displays a loss message"""
    assert "RIP" in game_view_1._get_game_over_display(game_controller_1)