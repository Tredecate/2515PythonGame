from models.player import Player

class GameView:
    """ Class that handles displaying the game to the user """

    def __init__(self, player: Player):
        """ Instantiates the GameView class
        
        Args:
            player (Player): The player object for this session 
        """
        self._player = player
    
    def render(self, current_map: list):
        """ Prints the current game view as returned by a private function
        
        Args:
            current_map (2D list): The current map-state 
        """
        print(self._get_map_display(current_map))

    def render_game_over(self, game_controller):
        """ Prints a game over screen as returned by a private function
        
        Args:
            game_controller (GameController): The GameController for the current session 
        """
        print(self._get_game_over_display(game_controller))
    
    def _get_map_display(self, current_map: list):
        """ Returns the current state of the game for the player
        
        Args:
            current_map (2D list): The current map-state 
        """
        character_mapping = {"#": "█", "P": "☻", "I": "♫", "-": " ", "E": "♦"}
        rows_to_print = list()
        
        # map body
        for y in range(len(current_map[0])):
            row_to_print = "    |"

            for x in range(len(current_map)):
                row_to_print += character_mapping[current_map[x][y]] + (" " if x != len(current_map) - 1 else "")
            
            rows_to_print.append(row_to_print + "|    ")
    
        # header and footer
        rows_to_print.insert(0, "" + "=" * len(rows_to_print[0]))
        rows_to_print.insert(0, "" + f'{f"Points: {self._player.items}/5" : ^{len(rows_to_print[1])}}')
        rows_to_print.insert(0, "\n" + "=" * len(rows_to_print[2]))
        rows_to_print.append("=" * len(rows_to_print[3]))

        # stringify list
        output = ""

        for row in rows_to_print:
            output += row + "\n"
        
        return output.rstrip()

    def _get_game_over_display(self, game_controller):
        """ Returns a game over screen
        
        Args:
            game_controller (GameController): The GameController for the current session 
        """
        return f"{'GG, you won!' if game_controller.check_if_gg() else 'RIP, you lost...'}"