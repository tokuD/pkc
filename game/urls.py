from unicodedata import name
from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('tournament/list/', views.TournamentListView.as_view(), name='tournament_list'),
    path('tournament/enroll/<int:tournament_pk>/', views.EnrollTournamentView.as_view(), name='enroll_tournament'),
    path('tournament/create_game/<int:tournament_pk>/', views.CreateGameView.as_view(), name='create_game'),
    path('tournament/create_game/ajax/<int:tournament_pk>/', views.CreateGameAjaxView.as_view(), name='create_game_ajax'),
]
