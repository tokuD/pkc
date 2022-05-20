from django.db import models
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

class Tournament(models.Model):
    name = models.CharField(max_length=200, verbose_name='大会名')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='参加者', related_name='tournament', blank=True)
    start = models.DateTimeField(verbose_name='開始日時')
    finish = models.DateTimeField(verbose_name='終了日時')

    def __str__(self):
        return self.name

class PlayerToNum(models.Model):
    """大会ごとにplayerに通し番号を振る"""
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT, verbose_name='大会名')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='player')
    num = models.IntegerField(verbose_name='player番号')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tournament','num'],
                name='num_unique_for_tournament'
            )
        ]

    def __str__(self):
        return "{} - {} at {}".format(self.player, self.num, self.tournament)

class DeckThema(models.Model):
    name = models.CharField(verbose_name='デッキテーマ名', max_length=100)
    thumbnail = models.ImageField(verbose_name='テーマサムネイル', upload_to='themas/', blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(verbose_name='スキル名', max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    RESULT = [
        (1,"勝ち"),
        (-1,"負け"),
        (0,"引き分け")
    ]
    FIRST_SECOND = [
        (True,'先行'),
        (False,'後攻')
    ]
    tournament = models.ForeignKey(Tournament, verbose_name='大会名', on_delete=models.PROTECT, related_name='game')
    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='player1', related_name='game1', on_delete=models.PROTECT)
    finished_date = models.DateField(verbose_name='試合日付', default=timezone.now)
    finished_time = models.TimeField(verbose_name='終了時間', default=timezone.now)
    skill1 = models.ForeignKey(Skill, verbose_name='使用スキル', on_delete=models.PROTECT, related_name='game1')
    deck_thema1 = models.ForeignKey(DeckThema, verbose_name='使用テーマ', on_delete=models.PROTECT, related_name='game1')
    player2 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='対戦相手', on_delete=models.PROTECT, related_name='game')
    skill2 = models.ForeignKey(Skill, verbose_name='相手スキル', on_delete=models.PROTECT, related_name='game2')
    deck_thema2 = models.ForeignKey(DeckThema, on_delete=models.PROTECT, related_name='game2', verbose_name='相手テーマ')
    first_second = models.BooleanField(verbose_name='先行or後攻', choices=FIRST_SECOND)
    result = models.IntegerField(verbose_name='勝敗', choices=RESULT)
    thema = models.CharField(verbose_name='テーマ相性用', max_length=100, blank=True)
    is_valid = models.BooleanField(verbose_name='is_valid', default=False)

    def __str__(self):
        # return "{} vs {} at {} {}".format(self.player1, self.player2, timezone.localtime(self.finished_date).strftime("%Y/%m/%d"), timezone.localtime(self.finished_time).strftime("%H:%M:%S"))
        return f'{self.finished_date.strftime("%Y/%m/%d")} {self.finished_time.strftime("%H:%M:%S")}'

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse('game:create_game', kwargs={'tournament_pk': self.tournament.pk}))
