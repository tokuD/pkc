import json, csv
from django.shortcuts import render
from django.views import generic
from django.utils import timezone

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
