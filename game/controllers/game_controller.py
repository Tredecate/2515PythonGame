import requests

from models.maze import Maze
from models.player import Player
from views.game_view import GameView

API_URL = "http://localhost:5000/api"

class GameController:
    """ Controller to handle the general game loop actions """

    def __init__(self, maze: Maze):
        """ Instantiates the GameController
        
        Args:
            maze (Maze): The maze the current session is using 
        """
        self._ticks_since_move = 0

        self._maze = maze
        self._maze.populate()

        self._player = Player(self._maze)

        self._game_view = GameView(self._player, self, self._maze.state)
        self._game_view.render(self._maze)
    
    def tick(self, next_action):
        """ Main game logic function. Tells view to render, gets user input from player controller,
            tells the Player object to move depending on input, and keeps track of the game win/loss state.
        
        Args:
            next_action (str): The current player input

        Raises:
            SystemExit: The player finished the game 
        """
        if self._ticks_since_move / 10 >= 1:
            current_tile = ""

            if next_action == "w":
                current_tile = self._player.move(self._player.pos[0], self._player.pos[1] - 1)
                self._ticks_since_move = -1
            elif next_action == "s":
                current_tile = self._player.move(self._player.pos[0], self._player.pos[1] + 1)
                self._ticks_since_move = -1
            elif next_action == "a":
                current_tile = self._player.move(self._player.pos[0] - 1, self._player.pos[1])
                self._ticks_since_move = -1
            elif next_action == "d":
                current_tile = self._player.move(self._player.pos[0] + 1, self._player.pos[1])
                self._ticks_since_move = -1

            if (current_tile == "E"):
                # Player stepped on end flag
                self._game_view.render_game_over(self)
                raise SystemExit

        self._ticks_since_move += 1

    def check_if_gg(self, timer):
        """ Checks if player has collected all the items in the maze
        
        Args:
            timer (int): The amount of time left
        
        Returns: (bool) True if there are no more items in the maze 
        """
        return len(self._maze.locate_object("I")) == 0 and timer > 0
    
    def process_score(self, timer, name):
        """ Calculates and sends a score to the API at API_URL
        
        Args:
            timer (int): The amount of time left
            name (str): The name of the player
        
        Returns: (bool) True if the score was successfully uploaded
        """
        try:
            req = requests.put(f"{API_URL}/new", json={"name": name, "score": timer * self._player.items})
            return int(req.status_code) == 204
        except:
            return False