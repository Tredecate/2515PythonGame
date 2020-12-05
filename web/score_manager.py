from score import Score
from csv import DictReader, DictWriter
from json import dumps, loads

class ScoreManager:
    def __init__(self):
        """ Initializes our score manager """
        self._scores = list()

    def __len__(self):
        """ returns the length of score list"""
        return len(self._scores)

    @property
    def scores(self):
        """ Returns a list of dictionaries (state of Score objects) """
        return [score.to_dict() for score in sorted(self._scores, reverse=True)]

    def add_score(self, score):
        """ Adds a score to the manager """
        if type(score) is not Score:
            raise TypeError("Cannot add a non-score object to the manager")

        self._scores.append(score)

    def remove_user_score(self, name):
        """ Removes all scores from the given user

        Args:
            name (string): The name of the user to delete the scores of
        """
        self._scores = [score for score in self._scores if score.name != name]

    def serialize(self):
        """ Returns a list of dictionaries (state of Score objects) """
        return self.scores

    def to_csv(self, filename):
        """ Stores the contents of this manager in a CSV file with the given name """
        if type(filename) is not str or len(filename) == 0:
            raise ValueError("Incorrect arguments")

        with open(filename, "w") as file:
            writer = DictWriter(file, fieldnames=["name", "score"])
            writer.writeheader()
            writer.writerows(self.scores)

    def to_json(self, filename):
        """ Stores the contents of this manager in a JSON file with the given name """
        if type(filename) is not str or len(filename) == 0:
            raise ValueError("Incorrect arguments")

        with open(filename, "w") as file:
            file.write(dumps({"scores": self.scores}))

    def from_csv(self, filename):
        """ Loads the contents of the given CSV file into this ScoreManager """
        if type(filename) is not str or len(filename) == 0:
            raise ValueError("Incorrect arguments")

        with open(filename, "r") as file:
            reader = DictReader(file.readlines())
            for row in reader:
                self.add_score(Score(row["name"], int(row["score"])))

    def from_json(self, filename):
        """ Loads the contents of the given JSON file into this ScoreManager """
        if type(filename) is not str or len(filename) == 0:
            raise ValueError("Incorrect arguments")

        with open(filename, "r") as file:
            self._scores = [Score(score["name"], score["score"]) for score in (loads(file.read())["scores"])]