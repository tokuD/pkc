from dataclasses import fields
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportMixin


from . import models


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'finish']

@admin.register(models.PlayerToNum)
class PlayerToNumAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'player', 'num']

@admin.register(models.DeckThema)
class DeckThemaAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']

class GameResource(resources.ModelResource):
    player1 = fields.Field(column_name='player1')
    player2 = fields.Field(column_name='player2')
    skill1 = fields.Field(column_name='player1スキル')
    skill2 = fields.Field(column_name='player2スキル')
    deck_thema1 = fields.Field(column_name='player1使用テーマ')
    deck_thema2 = fields.Field(column_name='player2使用テーマ')
    first_second = fields.Field(column_name='先行or後攻')
    result = fields.Field(column_name='勝敗')
    tournament = fields.Field(column_name='大会名')

    def dehydrate_player1(self, data: models.Game):
        return data.player1.username

    def dehydrate_player2(self, data: models.Game):
        return data.player2.username

    def dehydrate_skill1(self, data: models.Game):
        return data.skill1.name

    def dehydrate_skill2(self, data: models.Game):
        return data.skill2.name

    def dehydrate_deck_thema1(self, data: models.Game):
        return data.deck_thema1.name

    def dehydrate_deck_thema2(self, data: models.Game):
        return data.deck_thema2.name

    def dehydrate_first_second(self, data: models.Game):
        return '先行' if data.first_second else '後攻'

    def dehydrate_result(self, data: models.Game):
        RESULT={1:'勝ち',-1:'負け',0:'引き分け'}
        return RESULT[data.result]

    def dehydrate_tournament(self, data: models.Game):
        return data.tournament.name

    class Meta:
        model = models.Game
        fields = ['tournament', 'finished', 'player1', 'player2', 'skill1', 'skill2', 'deck_thema1', 'deck_thema2', 'first_second', 'result']

@admin.register(models.Game)
class GameAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = GameResource
    list_display = ['tournament', 'player1', 'player2', 'finished', 'result']
    list_filter = ['tournament']
