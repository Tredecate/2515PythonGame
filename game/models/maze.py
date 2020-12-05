from copy import deepcopy
from random import randint

class Maze:
    """ Represents a Maze """

    def __init__(self, grid: list):
        """ Instantiates a Maze from the given 2D list
        
        Args:
            grid (2D list): 2D list representing the maze
        """
        self._maze_map = grid
    
    @property
    def state(self):
        """ Returns a copy of the current map state as a 2D list """
        return deepcopy(self._maze_map)

    def check_if_empty(self, x: int, y: int, ignore_obj=True):
        """ Checks if the given cell is empty
        
        Args:
            x (int): The X coordinate of the cell to check
            y (int): The Y coordinate of the cell to check
            ignore_obj (bool): Whether or not to ignore Players/Items (default: True)
        
        Returns: (bool) Whether or not the given cell is empty 
        """
        if not self._valid_coord(x, y):
            return False
        
        return (self._maze_map[x][y] == "-") or (ignore_obj and self._maze_map[x][y] != "#")
    
    def set_cell(self, x: int, y: int, char: str):
        """ Sets the target cell to a specified character 
        
        Args:
            x (int): The X coordinate of the cell to set
            y (int): The Y coordinate of the cell to set
            char (str): The character to set the cell to.

        Valid characters:
            P: player
            I: item
            O: empty item
            -: empty space
            #: wall 
        
        Returns: (str) The character that was previously at this cell
        """
        if not self._valid_coord(x, y):
            return

        if char in ("P", "I", "-", "#", "O"):
            old_char = self._maze_map[x][y]
            self._maze_map[x][y] = char

            return old_char
    
    def populate(self, item_amount=5):
        """ Populates the maze with items
        
        Args:
            item_amount (int): How many items to add to the maze (default: 5) 
        """
        populated = 0

        while populated < item_amount:
            rx = randint(0, len(self._maze_map))
            ry = randint(0, len(self._maze_map[0]))

            if self.check_if_empty(rx, ry, False):
                self.set_cell(rx, ry, "I")
                populated += 1
    
    def locate_object(self, char: str):
        """ Returns a list of coordinates for each instance of the specified character 
        
        Args:
            char (str): The character to search for

        Valid characters:
            P: player
            I: item
            -: empty space
            #: wall 
        """
        instances = list()

        for row_index, row in enumerate(self._maze_map):
            for col_index, col in enumerate(row):
                if col == char:
                    instances.append((row_index, col_index))
        
        return instances
    
    def _valid_coord(self, x: int, y: int):
        """ Returns true if the given coordinates are valid """
        return x < len(self._maze_map) and x >= 0 and y < len(self._maze_map[0]) and y >= 0
    
    @classmethod
    def load_from_file(self, filename: str):
        """ Loads the maze grid from the given file and returns a Maze object
        
        Args:
            filename: the file to open
        
        Raises:
            ValueError: Specified filename cannot be found
            RuntimeError: The column width throughout the maze doesn't match the first line 
        """
        try:
            maze_txt = open(filename)
        except FileNotFoundError:
            raise ValueError(f"Cannot find file: {filename}")

        maze_file = maze_txt.read()
        maze_txt.close()

        maze_map = [list() for _ in maze_file.splitlines()[0]]

        for x in range(len(maze_file.splitlines()[0])):
            for line in maze_file.splitlines():
                try:
                    maze_map[x].append(line[x])
                except:
                    raise RuntimeError("The maze isn't rectangular!")
                
        return Maze(maze_map)