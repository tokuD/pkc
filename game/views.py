import datetime
import json, csv
from operator import index
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth import get_user_model, mixins
from django.contrib import messages
from django.urls import reverse
from django_pandas.io import read_frame


from . import models, analysis


class TournamentListView(generic.ListView):
    model = models.Tournament
    template_name = 'game/tournament_list.html'


class EnrollTournamentView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Tournament
    template_name = 'game/enroll_tournament.html'
    pk_url_kwarg = 'tournament_pk'

    def post(self, request, *args, **kwargs):
        input_password = request.POST.get('password')
        tournament_pk = self.kwargs.get('tournament_pk')
        tournament = models.Tournament.objects.get(pk=tournament_pk)
        if input_password:
            players = models.PlayerToNum.objects.filter(tournament=tournament).count()
            models.PlayerToNum.objects.create(
                tournament=tournament,
                player=self.request.user,
                num=players+1
            )
            tournament.participants.add(self.request.user)
            return HttpResponseRedirect(reverse('game:create_game', kwargs={'tournament_pk': tournament_pk}))
        else:
            return HttpResponseRedirect(reverse('game:enroll_tournament', kwargs={'tournament_pk': tournament_pk}))



class CreateGameView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'game/create_game.html'

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
        analyser = analysis.Analysis(self.kwargs.get('tournament_pk'), self.request.user)
        themas = analyser.get_distribution()
        dps = analyser.get_dp()
        if request.GET.get('table'):
            tables = analyser.get_tables()
            return JsonResponse({'themas': themas, 'dps': dps, 'tables': tables}, safe=False)
        return JsonResponse({'themas': themas, 'dps': dps}, safe=False)

    def post(self, request, *args, **kwargs):
        hour = request.POST.get('finished_time').split(':')[0]
        minute = request.POST.get('finished_time').split(':')[1]
        tournament=models.Tournament.objects.get(pk=self.kwargs.get('tournament_pk'))
        result = request.POST.get('result')
        thema1 = models.DeckThema.objects.get(pk=request.POST.get('deck_thema1'))
        thema2 = models.DeckThema.objects.get(pk=request.POST.get('deck_thema2'))
        thema = ''
        if int(result) == 1: thema = "{},{}".format(thema1.name, thema2.name)
        elif int(result) == -1: thema = "{},{}".format(thema2.name, thema1.name)
        models.Game.objects.create(
            tournament=tournament,
            player1=self.request.user,
            finished_time=datetime.time(int(hour), int(minute), 0, 0),
            skill1=models.Skill.objects.get(pk=request.POST.get('skill1')),
            deck_thema1=thema1,
            player2=get_user_model().objects.get(pk=request.POST.get('player2')),
            skill2=models.Skill.objects.get(pk=request.POST.get('skill2')),
            deck_thema2=thema2,
            first_second=request.POST.get('first_second'),
            result=int(result),
            thema=thema
        )
        analyser = analysis.Analysis(self.kwargs.get('tournament_pk'), self.request.user)
        themas = analyser.get_distribution()
        dps = analyser.get_dp()
        tables = analyser.get_tables()
        return JsonResponse({'themas': themas, 'dps': dps, 'tables': tables, 'success': True, 'message': '保存しました。'}, safe=False)


class CsvExportView(mixins.LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        tournament_pk = self.kwargs.get('tournament_pk')
        tournament = models.Tournament.objects.get(pk=tournament_pk)
        query = models.Game.objects.filter(tournament=tournament)
        response = HttpResponse(content_type='text/csv; charset=CP932')
        response['Content-Disposition'] = 'attachment; filename={}_{}.csv'.format(tournament.name,timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S"))
        df = read_frame(query)
        df.to_csv(path_or_buf=response, encoding='utf_8_sig', index=None)
        return response


class MyPageView(mixins.LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = 'mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = models.Tournament.objects.filter(participants=self.request.user)
        context.update({'object_list': object_list})
        return context
