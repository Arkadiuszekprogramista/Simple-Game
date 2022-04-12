import pytest
from django.contrib.auth.models import User
from monsterfigther_app.models import PlayerMonster
from django.urls import reverse


@pytest.mark.django_db
def test_creating_monster_view(client, example_create_monster):
    client.login(username='test1', password='test1')
    client.post('player/345/create_monster/'), {
        'name': 'PlayerMonster345',
    }
    assert PlayerMonster.objects.get(
        name='PlayerMonster345'
    )

@pytest.mark.django_db
def test_main_view(client):
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_view(client):
    response = client.post('/login/', {'username': 'test1', 'password': 'test1'})
    assert response.status_code == 200

@pytest.mark.django_db
def test_set_new_password_view(client, example_user):
    client.force_login(example_user)
    response = client.post(f'/login/resetpass/{example_user.id}/', {
        'new_pass1': 'newpassTest',
        'new_pass2': 'newpassTest',
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_item_details_view(client, example_item, example_user):
    client.force_login(example_user)
    response = client.get(f'/item/{example_item.slug}/')
    assert response.status_code == 200
    assert response.context['item'][0].name == example_item.name
    assert response.context['item'][0].description == example_item.description
    assert response.context['item'][0].modification_to_attack == example_item.modification_to_attack
    assert response.context['item'][0].bonuses_to_life == example_item.bonuses_to_life
    assert response.context['item'][0].slug == example_item.slug

@pytest.mark.django_db
def test_abilities_details_view(client, example_abilities, example_user):
    client.force_login(example_user)
    response = client.get(f'/skill/{example_abilities.slug}/')
    assert response.status_code == 200
    assert response.context['skill'][0].name == example_abilities.name
    assert response.context['skill'][0].description == example_abilities.description
    assert response.context['skill'][0].damage == example_abilities.damage
    assert response.context['skill'][0].heal == example_abilities.heal
    assert response.context['skill'][0].modification == example_abilities.modification

@pytest.mark.django_db
def test_numbers_of_items(example_user, client, example_five_items):
    client.force_login(example_user)
    url = reverse('items-list')
    response = client.get(url)
    assert response.status_code == 200
    context = response.context
    assert context['item'].count() == len(example_five_items)
    for item in example_five_items:
        assert item in context['item']

@pytest.mark.django_db
def test_numbers_of_abilities(example_user, client, example_five_abilities):
    client.force_login(example_user)
    url = reverse('abilities-list')
    response = client.get(url)
    assert response.status_code == 200
    context = response.context
    assert context['skill'].count() == len(example_five_abilities)
    for item in example_five_abilities:
        assert item in context['skill']

@pytest.mark.django_db
def test_registration(client):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    client.post(url, {
        'username': 'Player44',
        'pass1': 'Player44',
        'pass2': 'Player44',
        'email': 'Player44@Player44.Player44',
        'first_name': 'Player44',
        'last_name': 'Player44',
        'stage': 1,
    })
    assert User.objects.get(username='Player44')

@pytest.mark.django_db
def test_newgame_view(client, example_player,example_user):
    client.force_login(example_user)
    response = client.get(f'/newgame/{example_player.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_gameover_view(client, example_player, example_user):
    client.force_login(example_user)
    response = client.get(f'/gameover/{example_player.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_player_details_view(client, example_user, example_player, example_item):
    client.force_login(example_user)
    response = client.get(f'/player/{example_player.id}/')
    assert response.status_code == 200
    assert response.context['player'].user.username == 'test2'
    assert response.context['player'].current_stage == 1
    assert response.context['player'].player_monster.name == 'PlayerMonster'

@pytest.mark.django_db
def test_monster_details_view(client, example_player, example_create_monster, example_user, example_item, example_abilities):
    client.force_login(example_user)
    response = client.get(f'/player/{example_player.id}/monster_details/')
    assert response.status_code == 200
    assert response.context['monster'].name == 'PlayerMonster'
    assert response.context['monster'].life == 300
    assert response.context['monster'].attack == 100
    assert response.context['monster'].max_life == 300
    assert response.context['monster'].description == 'monster description'

@pytest.mark.django_db
def test_update_monster_item_view(example_player, client, example_user, example_create_monster):
    client.force_login(example_user)
    response = client.get(f'/player/{example_create_monster.pk}/monster_items/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_monster_abilities_view(example_user, client, example_create_monster):
    client.force_login(example_user)
    response = client.get(f'/player/{example_create_monster.pk}/monster_abilities/')
    assert response.status_code == 200
