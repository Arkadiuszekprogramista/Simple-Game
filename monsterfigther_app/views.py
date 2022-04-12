from django.views import View
from django.shortcuts import render, redirect
from monsterfigther_app.forms import LoginForm, RegistrationForm, CreatePlayerMonsterForm, ResetPasswordIfLoggedForm, \
    UpdateMonsterItemsForm, UpdateMonsterSkillsForm, Attack1ButtonForm, Attack2ButtonForm, Attack3ButtonForm,\
    NewGameForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from monsterfigther_app.models import Player, Items, PlayerMonster, Abilities, Enemies
from django.views.generic import ListView, UpdateView

# Base view
class MainView(View):
    def get(self, request):
        return render(request, 'base.html')

# Login view
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'form': form})
            else:
                login(request, user)
                return redirect('/')

# Logout view only redirect
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

# Resset password for logged players/users
class RessetPasswordView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        player = Player.objects.get(id=user_id)
        form = ResetPasswordIfLoggedForm
        return render(request, 'reset_password.html', {
            'form': form,
            'player': player,
        })

    def post(self, request, user_id):
        form = ResetPasswordIfLoggedForm(request.POST)
        user = User.objects.get(id=user_id)
        if form.is_valid():
            password = form.cleaned_data['new_pass1']
            user.set_password(password)
            user.save()
            return redirect('/')

# Registration User/Player
class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration_form.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['pass1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            stage = form.cleaned_data['stage']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            Player.objects.create(current_stage=stage, user=user)
            return redirect('/')
        else:
            return render(request, 'registration_form.html', {'form': form})

# Details view of Player items, monster adn current stage
class PlayerDetailsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        player = Player.objects.get(id=user_id)
        item = Items.objects.filter(playermonster__id=user_id)
        return render(request, 'player_details.html', {
            'player': player,
            'items': item,
        })

# Viw white form to create monster, choose name ,and select on of three kind of monster to play
class CreatePlayerMonsterView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        form = CreatePlayerMonsterForm
        return render(request, 'create_monster.html', {'form': form})

    def post(self, request, user_id):
        form = CreatePlayerMonsterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            monster = form.cleaned_data['monster']
            player = Player.objects.get(id=user_id)

            if monster == PlayerMonster.objects.get(id=1):
                life = monster.life
                attack = monster.attack
                description = monster.description
                current_life = monster.current_life
                max_life = monster.max_life
                new_monster = PlayerMonster.objects.create(
                    name=name,
                    life=life,
                    attack=attack,
                    description=description,
                    current_life=current_life,
                    max_life=max_life,
                )
                player.player_monster = new_monster
                player.save()

            elif monster == PlayerMonster.objects.get(id=2):
                life = monster.life
                attack = monster.attack
                description = monster.description
                current_life = monster.current_life
                max_life = monster.max_life
                new_monster = PlayerMonster.objects.create(
                    name=name,
                    life=life,
                    attack=attack,
                    description=description,
                    current_life=current_life,
                    max_life=max_life,
                )
                player.player_monster = new_monster
                player.save()

            elif monster == PlayerMonster.objects.get(id=3):
                life = monster.life
                attack = monster.attack
                description = monster.description
                current_life = monster.current_life
                max_life = monster.max_life
                new_monster = PlayerMonster.objects.create(
                    name=name,
                    life=life,
                    attack=attack,
                    description=description,
                    current_life=current_life,
                    max_life=max_life,
                )
                player.player_monster = new_monster
                player.save()

            return redirect('/')
        else:
            return render(request, 'create_monster.html', {'form': form})

# Details view of Monster items, abilities and statistics
class MonsterDetailsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        player = Player.objects.get(id=user_id)
        monster_details = PlayerMonster.objects.get(player=user_id)
        items = Items.objects.filter(playermonster__id=user_id)
        skill = Abilities.objects.filter(playermonster__id=user_id)

        return render(request, 'monster_details.html', {
            'monster': monster_details,
            'items': items,
            'skills': skill,
            'player': player,
        })

# Detail of item: name, modification, description etc.
class ItemDetailsView(LoginRequiredMixin, ListView):
    model = Items
    template_name = 'item_details.html'
    context_object_name = 'item'
    paginate_by = 3

    def get_queryset(self):
        return Items.objects.filter(slug=self.kwargs['slug'])

# Detail of ability: name, modification, description etc.
class AbilitiesDetailsView(LoginRequiredMixin, ListView):
    model = Abilities
    template_name = 'abilities_details.html'
    context_object_name = 'skill'
    paginate_by = 3

    def get_queryset(self):
        return Abilities.objects.filter(slug=self.kwargs['slug'])

# Form to change items on monster, max three monster can wear
class UpdateMonsterItemsView(LoginRequiredMixin, UpdateView):
    form_class = UpdateMonsterItemsForm
    template_name = 'items_update_form.html'
    success_url = '/'

    def get_queryset(self):
        return PlayerMonster.objects.all().order_by('id')

# Form to change skill on monster, max three monster use
class UpdateMonsterSkillView(LoginRequiredMixin, UpdateView):
    form_class = UpdateMonsterSkillsForm
    template_name = 'abilities_update_form.html'
    success_url = '/'

    def get_queryset(self):
        return PlayerMonster.objects.all().order_by('id')

# calculating all bonuses to life from items to monster
def adding_life_bonuses_from_items(queryset):
    suma_life_bonus = 0
    for i in range(len(queryset)):
        suma_life_bonus += queryset[i]['bonuses_to_life']
    return suma_life_bonus

# calculating all bonuses to attack from items to monster
def adding_attack_modification_from_items(queryset):
    suma_mod_attack = 0
    for i in range(len(queryset)):
        suma_mod_attack += queryset[i]['modification_to_attack']
    return suma_mod_attack

# calculating power of attack for each skill monster use
def adding_skill_damage_to_attack(queryset):
    suma_skill_damage = 0
    for i in range(len(queryset)):
        suma_skill_damage += queryset[i]['damage']

# calculating power of heal for each skill monster use
def adding_skill_heal_to_attack(queryset):
    suma_skill_heal = 0
    for i in range(len(queryset)):
        suma_skill_heal += queryset[i]['heal']

# List of abilities that are in game
class AbilitiesDetailsListView(LoginRequiredMixin, ListView):
    model = Abilities
    template_name = 'abilities_details.html'
    context_object_name = 'skill'
    paginate_by = 3

# List of items that are in game
class ItemDetailsListView(LoginRequiredMixin, ListView):
    model = Items
    template_name = 'item_details.html'
    context_object_name = 'item'
    paginate_by = 3

# Combat Zone, by clicking a button you monster will attack or heal
class CombatZoneView(LoginRequiredMixin, View):

    def get(self, request, player_id):
        player = Player.objects.get(id=player_id)
        enemy = Enemies.objects.get(id=player.current_stage)
        monster = PlayerMonster.objects.get(player=player_id)
        items = Items.objects.filter(playermonster=player_id).values('bonuses_to_life', 'modification_to_attack')
        skill = Abilities.objects.filter(playermonster__id=player_id).values('damage', 'heal')
        skill_name = Abilities.objects.filter(playermonster__id=player_id)

        max_life = monster.life + adding_life_bonuses_from_items(items)
        monster_current_attack = monster.attack + adding_attack_modification_from_items(items)

        if player.current_stage == 1 and enemy.current_life == enemy.max_life:
            monster.current_life = max_life
            monster.save()

        attack1 = monster.attack + adding_attack_modification_from_items(items) + skill[0]['damage']
        try:
            attack2 = monster.attack + adding_attack_modification_from_items(items) + skill[1]['damage']
        except:
            attack2 = None
        try:
            attack3 = monster.attack + adding_attack_modification_from_items(items) + skill[2]['damage']
        except:
            attack3 = None
        heal1 = monster.attack + adding_attack_modification_from_items(items) + skill[0]['heal']

        try:
            heal2 = monster.attack + adding_attack_modification_from_items(items) + skill[1]['heal']
        except:
            heal2 = None
        try:
            heal3 = monster.attack + adding_attack_modification_from_items(items) + skill[2]['heal']
        except:
            heal3 = None

        form1 = Attack1ButtonForm()
        form2 = Attack2ButtonForm()
        form3 = Attack3ButtonForm()

        return render(request, 'combat_zone.html', {
            'player': player,
            'monster': monster,
            'skill_name': skill_name,
            'enemy': enemy,
            'max_life': max_life,
            'monster_current_attack': monster_current_attack,
            'form1': form1,
            'form2': form2,
            'form3': form3,

            'attack1': attack1,
            'attack2': attack2,
            'attack3': attack3,

            'heal1': heal1,
            'heal2': heal2,
            'heal3': heal3,
        })

    def post(self, request, player_id):


        player = Player.objects.get(id=player_id)
        enemy = Enemies.objects.get(id=player.current_stage)
        monster = PlayerMonster.objects.get(player=player_id)
        items = Items.objects.filter(playermonster=player_id).values('bonuses_to_life', 'modification_to_attack')
        skill = Abilities.objects.filter(playermonster__id=player_id).values('damage', 'heal')
        max_life = monster.life + adding_life_bonuses_from_items(items)

        attack1 = monster.attack + adding_attack_modification_from_items(items) + skill[0]['damage']
        try:
            attack2 = monster.attack + adding_attack_modification_from_items(items) + skill[1]['damage']
        except:
            attack2 = None
        try:
            attack3 = monster.attack + adding_attack_modification_from_items(items) + skill[2]['damage']
        except:
            attack3 = None

        heal1 = monster.attack + adding_attack_modification_from_items(items) + skill[0]['heal']
        try:
            heal2 = monster.attack + adding_attack_modification_from_items(items) + skill[1]['heal']
        except:
            heal2 = None
        try:
            heal3 = monster.attack + adding_attack_modification_from_items(items) + skill[2]['heal']
        except:
            heal3 = None

        form1 = Attack1ButtonForm(request.POST)

        if 'form1' in request.POST:

            if form1.is_valid():
                monster.current_life = monster.current_life - enemy.attack
                if monster.current_life < enemy.attack:
                    monster.current_life = max_life
                    enemy.current_life = enemy.max_life
                    player.current_stage = 1
                    player.save()
                    enemy.save()
                    monster.save()
                    return redirect(f'/gameover/{player_id}/')
                monster.current_life = monster.current_life + heal1
                if monster.current_life > max_life:
                    monster.current_life = max_life
                monster.save()

                enemy.current_life = enemy.current_life - attack1
                if enemy.current_life < attack1:
                    enemy.current_life = enemy.life
                    player.current_stage = player.current_stage + 1
                    if player.current_stage > 9:
                        return redirect(f'/newgame/{player_id}/')
                    player.save()
                    enemy.save()
                else:
                    enemy.save()
                return redirect(f'/player/{player_id}/combat/')
            else:
                redirect('/')

        form2 = Attack2ButtonForm(request.POST)

        if 'form2' in request.POST:

            if form2.is_valid():
                monster.current_life = monster.current_life - enemy.attack
                if monster.current_life < enemy.attack:
                    monster.current_life = max_life
                    enemy.current_life = enemy.max_life
                    player.current_stage = 1
                    player.save()
                    enemy.save()
                    monster.save()
                    return redirect(f'/gameover/{player_id}/')
                monster.current_life = monster.current_life + heal2
                if monster.current_life > max_life:
                    monster.current_life = max_life
                monster.save()

                enemy.current_life = enemy.current_life - attack2
                if enemy.current_life < attack2:
                    enemy.current_life = enemy.life
                    player.current_stage = player.current_stage + 1
                    if player.current_stage > 9:
                        return redirect(f'/newgame/{player_id}/')
                    player.save()
                    enemy.save()
                else:
                    enemy.save()
                return redirect(f'/player/{player_id}/combat/')
            else:
                redirect('/')

        form3 = Attack3ButtonForm(request.POST)

        if 'form3' in request.POST:

            if form3.is_valid():
                monster.current_life = monster.current_life - enemy.attack
                if monster.current_life < enemy.attack:
                    monster.current_life = max_life
                    enemy.current_life = enemy.max_life
                    player.current_stage = 1
                    player.save()
                    enemy.save()
                    monster.save()
                    return redirect(f'/gameover/{player_id}/')
                monster.current_life = monster.current_life + heal3
                if monster.current_life > max_life:
                    monster.current_life = max_life
                monster.save()

                enemy.current_life = enemy.current_life - attack3
                if enemy.current_life < attack3:
                    enemy.current_life = enemy.life
                    player.current_stage = player.current_stage + 1
                    if player.current_stage > 9:
                        return redirect(f'/newgame/{player_id}/')
                    player.save()
                    enemy.save()
                else:
                    enemy.save()
                return redirect(f'/player/{player_id}/combat/')
            else:
                redirect('/')

# Clik Yes for New Game
class NewGameView(LoginRequiredMixin, View):
    def get(self, request, player_id):
        form = NewGameForm()
        return render(request, 'new_game.html', {'form': form})

    def post(self, request, player_id):
        form = NewGameForm(request.POST)
        if form.is_valid():
            player = Player.objects.get(id=player_id)
            monster = PlayerMonster.objects.get(player=player_id)
            if form.cleaned_data['YES'] == True:
                items = Items.objects.filter(playermonster=player_id).values('bonuses_to_life', 'modification_to_attack')
                last_boss = Enemies.objects.get(id=9)
                last_boss.current_life = last_boss.max_life
                max_life = monster.life + adding_life_bonuses_from_items(items)
                monster.current_life = max_life
                player.current_stage = 1
                player.save()
                monster.save()
                last_boss.save()
                return redirect('/')
            if form.cleaned_data['YES'] == False:
                return redirect('/')
            else:
                return render(request, 'new_game.html', {'form': form})

#You loose - game over
class GameOverView(LoginRequiredMixin, View):
    def get(self, request, player_id):
        return render(request, 'game_over.html')
