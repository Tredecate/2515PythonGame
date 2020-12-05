from models.maze import Maze
from models.player import Player

from views.game_view import GameView
from controllers.player_controller import PlayerController

class GameController:
    """ Controller to handle the general game loop actions """

    def __init__(self, maze: Maze):
        """ Instantiates the GameController
        
        Args:
            maze (Maze): The maze the current session is using 
        """
        self._maze = maze
        self._maze.populate()

        self._player = Player(self._maze)

        self._player_controller = PlayerController()
        self._game_view = GameView(self._player)
    
    def tick(self):
        """ Main game logic function. Tells view to render, gets user input from player controller,
            tells the Player object to move depending on input, and keeps track of the game win/loss state.
        Raises:
            SystemExit: The player finished the game 
        """
        self._game_view.render(self._maze.state)

        next_action = self._player_controller.process_input()
        current_tile = ""

        if next_action == "w":
            current_tile = self._player.move(self._player.pos[0], self._player.pos[1] - 1)
        elif next_action == "s":
            current_tile = self._player.move(self._player.pos[0], self._player.pos[1] + 1)
        elif next_action == "a":
            current_tile = self._player.move(self._player.pos[0] - 1, self._player.pos[1])
        elif next_action == "d":
            current_tile = self._player.move(self._player.pos[0] + 1, self._player.pos[1])

        if (current_tile == "E"):
            # Player stepped on end flag
            self._game_view.render(self._maze.state)
            self._game_view.render_game_over(self)
            raise SystemExit

    def check_if_gg(self):
        """ Checks if player has collected all the items in the maze
        
        Returns: (bool) True if there are no more items in the maze 
        """
        return len(self._maze.locate_object("I")) == 0