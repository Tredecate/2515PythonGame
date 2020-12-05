from models.maze import Maze

class Player:
    """ Represents a player """

    def __init__(self, maze: Maze):
        """ Instantiates the player
        
        Args:
            start_x (int): The starting x position of the player on the map
            start_y (int): The starting y position of the player on the map 
        """
        self._x, self._y = maze.locate_object("P")[0]
        self._maze = maze
        self._items = 0
    
    @property
    def pos(self):
        """ Returns the player's coordinates in a tuple (x, y) """
        return (self._x, self._y)
    
    @property
    def items(self):
        """ Returns how many items the player has picked up """
        return self._items
    
    def move(self, x: int, y: int):
        """ Tries to move the player to the specified location on the map
        
        Args:
            x (int): The x location to move the player to
            y (int): The y location to move the player to 
        
        Returns: (str) The character the player moved on top of
        """
        if self._maze.check_if_empty(x, y):

            if (x, y) in self._maze.locate_object("I"):
                self._items += 1

            self._maze.set_cell(self._x, self._y, "-")

            self._x = x
            self._y = y

            return self._maze.set_cell(x, y, "P")