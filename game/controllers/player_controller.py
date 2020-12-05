from models.player import Player

class PlayerController:
    """ Controller to handle processing player input """

    def __init__(self):
        """ Instantiates the PlayerController """
        self._first = True
    
    def process_input(self):
        """ Asks for user input until a valid action is entered
        
        Returns: (str) A single, lowercase character denoting what direction to go in 
        """
        query = "Enter Direction: "
        user_in = ""

        if self._first:
            query = "Collect all the ♫ and reach the ♦ to win!\nType a direction with W, A, S, or D, then press Enter: "
            self._first = False

        while user_in.lower() not in ("w", "a", "s", "d"):
            user_in = input(query)

        return user_in.lower()