import math
from collections import Counter
from . import models


class Analysis():

    def __init__(self, tournament_pk, user):
        tournament = models.Tournament.objects.get(pk=tournament_pk)
        self.games = models.Game.objects.filter(tournament=tournament).order_by('finished_date', 'finished_time')
        self.cleaned_games = self.game_valid()
        self.user = user

    def game_valid(self):
        for game in self.games:
            oppo = models.Game.objects.filter(
                player1=game.player2,
                finished_date=game.finished_date,
                finished_time=game.finished_time,
                skill1=game.skill2,
                deck_thema1=game.deck_thema2,
                player2=game.player1,
                skill2=game.skill1,
                deck_thema2=game.deck_thema1,
                first_second=not game.first_second,
                result=game.result * (-1),
                is_valid=False
            )
            if oppo.count() == 1:
                game.is_valid = True
                game.save()
        return self.games.filter(is_valid=True)


    def get_distribution(self):
        thema_names = Counter()
        themas = Counter()
        display_max = 5
        # for game in self.games:
        for game in self.cleaned_games:
            thema_names[game.deck_thema1.name] += 1
            thema_names[game.deck_thema2.name] += 1
            themas[game.deck_thema1] += 1
            themas[game.deck_thema2] += 1
        self.themas = sorted(themas.items(), key=lambda x:x[1], reverse=True)
        if len(self.themas) > display_max:
            self.themas = self.themas[:display_max]
        return sorted(thema_names.items(), key=lambda x:x[1], reverse=True)
        # return [('thema', count), ('thema', count), ...]

    def get_dp(self):
        dps = []
        dp = 0
        count = 0
        for game in self.games.filter(player1=self.user):
            count += 1
            if game.result == 1:
                dp += 1000
            elif game.result == -1:
                dp = max(0, dp-1000)
            dps.append((count, dp))
        return dps

    def get_tables(self):
        tables = []
        header = []
        for thema, count in self.themas:
            header.append({'name':thema.name, 'url':thema.thumbnail.url})
        tables.append(header)
        for thema1, count in self.themas:
            data = [{'name': thema1.name, 'url': thema1.thumbnail.url}]
            total_win = self.cleaned_games.filter(thema__istartswith="{},".format(thema1.name)).count()
            total_loose = self.cleaned_games.filter(thema__iendswith=",{}".format(thema1.name)).count()
            for thema2, count in self.themas:
                win = self.cleaned_games.filter(thema="{},{}".format(thema1.name, thema2.name)).count()
                loose = self.cleaned_games.filter(thema="{},{}".format(thema2.name, thema1.name)).count()
                col = {
                    'win': win,
                    'loose': loose,
                    'total': win+loose,
                    'rate': '{}%'.format(round((win/(win+loose))*100, 1)) if win+loose != 0 else '-'
                }
                data.append(col)
            data.append({
                'win': total_win,
                'loose': total_loose,
                'rate': '{}%'.format(round((total_win/(total_win+total_loose))*100, 1)) if total_win+total_loose != 0 else 'NO DATA'
            })
            tables.append(data)
        return tables

