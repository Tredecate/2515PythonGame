from score import Score


class ScoreManager:
    """ Simple class to manage a collection of scores
    
    Attributes:
        scores (list): the list of scores managed by the instance
    """

    def __init__(self):
        """ Initializes private attributes """
        self._scores = list()
    
    def __len__(self):
        """ Returns the length of the internal score list """
        return len(self._scores)
    
    @property
    def scores(self):
        """ Returns a list of the scores managed by this object """
        return [{"name": score.name, "score": score.score} for score in sorted(self._scores, reverse=True)]

    def add_score(self, score):
        """ Adds a score to the ScoreManager """
        if type(score) is not Score:
            raise TypeError("Invalid score.")

        self._scores.append(score)
    
    def remove_user_score(self, name):
        """ Removes all scores associated with the given name """
        len_before = len(self._scores)
        self._scores = [score for score in self._scores if score.name != name]

        # Return true if scores existed and were removed
        return len_before != len(self._scores)