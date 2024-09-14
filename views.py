


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Min
from django.shortcuts import render
from django.views import View
import datetime

from test_1.models import *

# Create your views here.



class Zadanie_2_View(LoginRequiredMixin, View):
    model = User
    template_name = "test_1/zadanie_1/zadanie_1.html"
    def get(self, request, *args, **kwargs):
        # Получим пользователя
        polzovatel = self.request.user

        # В данном случае не было задачи описывать как именно игрок проходит уровень. Просто создадим переменную
        # которая будет означать, что игрок прошел новый уровень и ему положен приз
        prize_add = 1
        if prize_add:
            Metods.Prizes(polzovatel)

        slovar_itog = {}

        return render(request, self.template_name, slovar_itog)


class Metods:

    @staticmethod
    def Prizes(polzovatel):
        user_0 = Player.objects.filter(player_id=polzovatel.pk).exists()
        if user_0:
            Metods.Prizes_vstavka_1(polzovatel)
        else:
            obj_1 = Player.objects.create(player_id=polzovatel.pk)
            obj_1.save()
            Metods.Prizes_vstavka_1(polzovatel)

    @staticmethod
    def Prizes_vstavka_1(polzovatel):
        igrok = Player.objects.get(player_id=polzovatel.pk)
        playerLevel_0 = PlayerLevel.objects.filter(player=igrok).exists()
        if playerLevel_0:
            Metods.Prizes_vstavka_2(igrok)
        else:
            min_level = Level.objects.aggregate(order=Min("order"))
            min_level_2 = Level.objects.filter(order=min_level["order"]).first()
            current_time = datetime.datetime.now().astimezone().date()
            obj_1 = PlayerLevel.objects.create(player=igrok, level=min_level_2, completed=current_time)
            obj_1.save()

    @staticmethod
    def Prizes_vstavka_2(igrok):
        playerLevel_1 = PlayerLevel.objects.filter(player=igrok).first()
        # Добавим уровень игроку
        # С начала найдем новый уровень для того что бы присвоить его игроку
        level_0 = playerLevel_1.level.order + 1
        level_1 = Level.objects.filter(order=level_0).exists()
        if level_1:
            level_2 = Level.objects.filter(order=level_0).first()
            playerLevel_1.level = level_2
            playerLevel_1.save()
            #  Я так понимаю приз это одно из свойств в таблице LevelPrize которое можно извлечь теперь уже.























