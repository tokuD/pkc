from collections import Counter
from . import models


class Distribution():

    def __init__(self, tournament_pk):
        tournament = models.Tournament.objects.get(pk=tournament_pk)
        self.games = models.Game.objects.filter(tournament=tournament)

    def get_distribution(self):
        themas = Counter()
        for game in self.games:
            themas[game.deck_thema1.name] += 1
            themas[game.deck_thema2.name] += 1
        return themas

