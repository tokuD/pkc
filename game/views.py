import datetime
import json, csv
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model, mixins
from django.contrib import messages


from . import models, analysis


class TournamentListView(generic.ListView):
    model = models.Tournament
    template_name = 'game/tournament_list.html'


class EnrollTournamentView(generic.DetailView):
    model = models.Tournament
    template_name = 'game/enroll_tournament.html'


class CreateGameView(generic.TemplateView):
    # model = models.Game
    template_name = 'game/create_game.html'
    # fields = ['finished', 'skill1', 'deck_thema1', 'player2', 'skill2', 'deck_thema2', 'first_second', 'result']

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
            'now': timezone.localtime(timezone.now()).strftime("%H:%M"),
            'skills': models.Skill.objects.all(),
            'themas': models.DeckThema.objects.all(),
            'player_and_num': player_and_num
        }
        context.update(data)
        return context


class CreateGameAjaxView(mixins.LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        return

    def post(self, request, *args, **kwargs):
        hour = int(request.POST.get('finished_time').split(':')[0])
        minute = int(request.POST.get('finished_time').split(':')[1])
        tournament=models.Tournament.objects.get(pk=self.kwargs.get('tournament_pk'))
        try:
            models.Game.objects.create(
                tournament=tournament,
                player1=self.request.user,
                finished_time=datetime.time(hour, minute, 0, 0),
                skill1=models.Skill.objects.get(pk=request.POST.get('skill1')),
                deck_thema1=models.DeckThema.objects.get(pk=request.POST.get('deck_thema1')),
                player2=get_user_model().objects.get(pk=request.POST.get('player2')),
                skill2=models.Skill.objects.get(pk=request.POST.get('skill2')),
                deck_thema2=models.DeckThema.objects.get(pk=request.POST.get('deck_thema2')),
                first_second=request.POST.get('first_second'),
                result=request.POST.get('result')
            )
        except:
            pass
        distribution = analysis.Distribution(self.kwargs.get('tournament_pk'))
        themas = distribution.get_distribution()
        return JsonResponse({'themas': themas}, safe=False)
