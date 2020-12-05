class Score:
    def __init__(self, name, value):
        """ Initiates our class
        
        Args:
            name (string): The name of the player who set this score
            value (int): The point-value of the score
        """
        if type(value) is not int:
            raise ValueError("Value is not an integer")
        if type(name) is not str:
            raise ValueError("Value is not a string")
        if not len(str(name)):
            raise ValueError("Invalid string")

        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def __str__(self):
        """ Returns a string representation of this score """
        return f"Score: {self._name} ({self._value})"

    def __lt__(self, other_score):
        if type(self) is not type(other_score):
            raise TypeError("Can't compare objects of different types")

        return self._value < other_score._value

    def to_dict(self):
        """ Returns a dictionary representation of this score """
        return {"name": self._name, "score": self._value}