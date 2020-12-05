class Score:
    """ Simple class to represent a score in a game """

    def __init__(self, name, score):
        """ Initializes private attributes

        Args:
            name (str): name of the player (cannot be empty)
            score (int): score of the player (cannot be negative)
        
        Raises:
            ValueError: name is empty or not string, score is not integer or negative
        """

        if type(name) is not str or not name:
            raise ValueError("Invalid name.")
        if type(score) is not int or score < 0:
            raise ValueError("Invalid score.")

        self._name = name
        self._score = score

    def __str__(self):
        """ Returns a string representation of the score """
        return f"Score: {self._name} ({self._score})"
    
    def __lt__(self, other):
        """ Allows for mathematical value comparisons """
        if type(other) is not type(self):
            raise TypeError("Unsupported type")

        return self._score < other._score
    
    @property
    def name(self):
        """ Returns the name associated with this score """
        return self._name
    
    @property
    def score(self):
        """ Returns the name associated with this score """
        return self._score