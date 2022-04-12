from django.contrib import admin
from monsterfigther_app.models import Player, Enemies, Items, PlayerMonster, Abilities

admin.site.register(Player),
admin.site.register(PlayerMonster),
admin.site.register(Enemies),
admin.site.register(Items),
admin.site.register(Abilities),
