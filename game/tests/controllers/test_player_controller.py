from controllers.player_controller import PlayerController
from unittest.mock import patch
from tests.fixtures import *


def test_class_definition(player_controller_1):
    """E0001 test class name == PlayerController"""
    assert type(player_controller_1) == PlayerController

@patch('builtins.input', return_value='D')
def test_process_input(input_func, player_controller_1):
    """D0002 ensure process_input() returns lower-cased correct input"""
    assert player_controller_1.process_input() == "d"