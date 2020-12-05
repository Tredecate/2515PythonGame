from models.maze import Maze
from controllers.game_controller import GameController

class App:
    """ This is the main class for our application

    It interacts with the Maze model and GameController
    """
    
    def __init__(self, filename="maze.txt"):
        """ Call the classmethod to load the map from the text file, then pass it into the GameController """
        try:
            self._game_controller = GameController(Maze.load_from_file(filename))
        except Exception as e:
            print("Could not start the game.")
            print(e)