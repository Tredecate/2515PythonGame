from models.maze import Maze
from tests.fixtures import *


def test_class_definition():
    """A0001 test class name == Maze"""
    assert type(Maze == Maze)

def test_parameter_value_validation():
    """A0002 filename has to exist"""
    with pytest.raises(ValueError):
        Maze.load_from_file("tttest.txt")

def test_parameter_type_validation():
    """A0003 maze must be rectangular"""
    with pytest.raises(RuntimeError):
        Maze.load_from_file("tests\\models\\test_maze_incorrect.txt")

def test_maze_initialization(maze_1):
    """A0004 valid arguments creates Maze object"""
    assert isinstance(maze_1, Maze)

def test_populate(maze_1):
    """A0005 populate adds 5 items to maze"""
    maze_1.populate()
    assert len(maze_1.locate_object('I')) == 6

def test_locate_object(maze_1):
    """A0006 locate_object returns list of correct coordinate tuples"""
    assert type(maze_1.locate_object('P')) == list
    assert maze_1.locate_object('P')[0] == (0, 0)
    assert len(maze_1.locate_object('P')) == 1
   

def test_set_cell_argument_validation(maze_1):
    """A0007 invalid coordinates or character return None"""
    assert maze_1.set_cell(10, 10, 'P') == None
    assert maze_1.set_cell(2, 2, 'F') == None
    

def test_set_cell(maze_1):
    """A0008 valid coordinates and character returns old character"""
    assert maze_1.set_cell(2, 2, 'P') == '-'


def test_check_if_empty_empty(maze_1):
    """A0009 location requested empty returns True"""
    assert maze_1.check_if_empty(1, 2) == True


def test_check_if_empty_item(maze_1):
    """A0010 location requested item returns True"""
    assert maze_1.check_if_empty(2, 0) == True


def test_check_if_empty_wall(maze_1):
    """A0011 location requested wall returns False"""
    assert maze_1.check_if_empty(5, 0) == False


def test_check_if_empty_outside(maze_1):
    """A0012 location requested outside returns False"""
    assert maze_1.check_if_empty(0, 7) == False


def test_state(maze_1):
    """A0013 state returns 2d array"""
    assert type(maze_1.state) == list
    assert type(maze_1.state[0]) == list
