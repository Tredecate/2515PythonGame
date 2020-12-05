from models.player import Player
from tests.fixtures import *


def test_class_definition(player_1):
    """B0001 test class name == Player"""
    assert type(player_1) == Player

def test_pos(player_1):
    """B0002 pos returns tuple containing correct position"""
    assert player_1.pos == (0, 0)

def test_items(player_1):
    """B0003 items returns correct integer corresponding to number of items obtained"""
    assert player_1.items == 0

def test_move(player_1):
    """B0004 move changes Player coordinates to correct location"""
    player_1.move(0, 1)
    assert player_1.pos == (0, 1)

def test_move_item_pickup(player_1):
    """B0005 move Player picks up item when Player coordinates match item's coordinates"""
    player_1.move(2, 0)
    assert player_1.items == 1
