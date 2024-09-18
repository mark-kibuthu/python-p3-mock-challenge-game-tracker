class Game:
    def __init__(self, title):
        if not isinstance(title, str) or len(title) == 0:
            raise ValueError("Title must be a non-empty string.")
        self._title = title
        self._results = []

    @property
    def title(self):
        return self._title

    # @title.setter
    # def title(self, value):
    #     if not isinstance(value, str):
    #         raise ValueError("Title must be a string.")
    #     self._title = value

    def results(self):
        return self._results

    def players(self):
        return list(set(result.player for result in self._results))

    def average_score(self, player):
        scores = [result.score for result in self._results if result.player == player]
        if not scores:
            return 0
        return sum(scores) / len(scores)

    def add_result(self, result):
        if not isinstance(result, Result):
            raise ValueError("Result must be an instance of Result.")
        if result.game != self:
            raise ValueError("Result's game must be this game instance.")
        self._results.append(result)

class Player:
    def __init__(self, username):
        if not isinstance(username, str) or not (2 <= len(username) <= 16):
            raise ValueError("Username must be a string between 2 and 16 characters long.")
        self._username = username
        self._results = []

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not isinstance(value, str):
            raise ValueError("Username must be a string.")
        if not (2 <= len(value) <= 16):
            raise ValueError("Username must be between 2 and 16 characters long.")
        self._username = value

    def results(self):
        return self._results

    def games_played(self):
        return list(set(result.game for result in self._results))

    def played_game(self, game):
        return game in self.games_played()

    def num_times_played(self, game):
        return sum(1 for result in self._results if result.game == game)

    def add_result(self, result):
        if not isinstance(result, Result):
            raise ValueError("Result must be an instance of Result.")
        if result.player != self:
            raise ValueError("Result's player must be this player instance.")
        self._results.append(result)

    @classmethod
    def highest_scored(cls, game):
        # Find player with highest average score for a given game
        players = set(result.player for result in game.results())
        if not players:
            return None
        return max(players, key=lambda p: game.average_score(p))

class Result:
    all = []

    def __init__(self, player, game, score):
        if not isinstance(score, int) or not (1 <= score <= 5000):
            raise ValueError("Score must be an integer between 1 and 5000 inclusive.")
        if not isinstance(player, Player):
            raise ValueError("Player must be an instance of Player.")
        if not isinstance(game, Game):
            raise ValueError("Game must be an instance of Game.")

        self._score = score
        self._player = player
        self._game = game

        # Add this result to the player's and game's results
        player.add_result(self)
        self._game.add_result(self)

        # Add this result to the class-level `all` list
        Result.all.append(self)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        raise AttributeError("Score is immutable and cannot be changed.")

    @property
    def player(self):
        return self._player

    @property
    def game(self):
        return self._game

    @classmethod
    def get_all_results(cls):
        return cls.all
