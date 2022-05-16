import json, csv
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model

from . import models


class TournamentListView(generic.ListView):
    model = models.Tournament
    template_name = 'game/tournament_list.html'


class EnrollTournamentView(generic.DetailView):
    model = models.Tournament
    template_name = 'game/enroll_tournament.html'


class CreateGameView(generic.CreateView):
    model = models.Game
    template_name = 'game/create_game.html'
    fields = ['finished', 'skill1', 'deck_thema1', 'player2', 'skill2', 'deck_thema2', 'first_second', 'result']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament_pk = self.kwargs.get('tournament_pk')
        player_and_num = []
        players = models.Tournament.objects.get(pk=tournament_pk).participants.all()
        for player in players:
            num = models.PlayerToNum.objects.get(tournament__pk=tournament_pk,player=player).num
            player_and_num.append(
                {'player': player, 'num': num}
            )
        data = {
            'now': timezone.localtime(timezone.now()),
            'skills': models.Skill.objects.all(),
            'themas': models.DeckThema.objects.all(),
            'player_and_num': player_and_num
        }
        context.update(data)
        return context