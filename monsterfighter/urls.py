
from django.contrib import admin
from django.urls import path
from monsterfigther_app.views import MainView, LoginView, LogoutView, RessetPasswordView, RegistrationView,\
    PlayerDetailsView, CreatePlayerMonsterView, MonsterDetailsView, ItemDetailsView, AbilitiesDetailsView, \
    CombatZoneView, UpdateMonsterItemsView, UpdateMonsterSkillView, ItemDetailsListView, AbilitiesDetailsListView,\
    NewGameView, GameOverView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/resetpass/<int:user_id>/', RessetPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('player/<int:user_id>/', PlayerDetailsView.as_view(), name='player-details'),
    path('player/<int:user_id>/create_monster/', CreatePlayerMonsterView.as_view(), name='create-monster'),
    path('player/<int:user_id>/monster_details/', MonsterDetailsView.as_view(), name='monster-details'),
    path('item/<slug:slug>/', ItemDetailsView.as_view(), name='item-details'),
    path('skill/<slug:slug>/', AbilitiesDetailsView.as_view(), name='abilities-details'),
    path('player/<int:pk>/monster_items/', UpdateMonsterItemsView.as_view(), name='change-items'),
    path('player/<int:pk>/monster_abilities/', UpdateMonsterSkillView.as_view(), name='change-abilities'),
    path('player/<int:player_id>/combat/', CombatZoneView.as_view(), name='combat-zone'),
    path('items/', ItemDetailsListView.as_view(),name='items-list'),
    path('skills/', AbilitiesDetailsListView.as_view(), name='abilities-list'),
    path('newgame/<int:player_id>/', NewGameView.as_view(), name='new-game'),
    path('gameover/<int:player_id>/', GameOverView.as_view(), name='game-over')

]
