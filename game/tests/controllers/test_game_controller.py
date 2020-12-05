from controllers.game_controller import GameController
from unittest.mock import patch
from tests.fixtures import *


def test_class_definition(game_controller_1):
    """D0001 test class name == GameController"""
    assert type(game_controller_1) == GameController

def test_gg_check(game_controller_1):
    """D0002 ensure check_if_gg() returns false when items are still in the maze"""
    assert game_controller_1.check_if_gg() == False

@patch.object(PlayerController, 'process_input')
def test_tick_raises_sysexit(mock_process_input, game_controller_1):
    """D0003 ensure tick() calls SystemExit when player moves and steps on an End object"""
    mock_process_input.return_value = "s"
    with pytest.raises(SystemExit):
        game_controller_1.tick()