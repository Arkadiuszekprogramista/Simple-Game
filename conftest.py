import pytest
from monsterfigther_app.models import Items, Abilities, PlayerMonster, User, Player, Enemies

@pytest.fixture
def example_create_monster():
    return PlayerMonster.objects.create(
        name='PlayerMonster345',
        life='300',
        attack='100',
        max_life=300,
        description='monster description',
    )

@pytest.fixture
def example_item():
    return Items.objects.create(
        name='Item 1', description='Item 1 description', bonuses_to_life=10, slug='item-1', modification_to_attack=1
    )

@pytest.fixture
def example_abilities():
    return Abilities.objects.create(
        name='Skill 1', description='Skill 1 description', damage=10, slug='skill-1', heal=1, modification='mod 1'
    )

@pytest.fixture
def example_user():
    return User.objects.create_user(
        username='test1',
        password='test1',
        email='test1@test1.test1',
        first_name='test1',
        last_name='test1',
    )

@pytest.fixture
def example_player():
    return Player.objects.create(
        user=User.objects.create(
            username='test2',
            password='test2',
            email='test2@test2.test2',
            first_name='test2',
            last_name='test2',
        ),
        current_stage=1,
        player_monster=PlayerMonster.objects.create(
            name='PlayerMonster',
            life=300,
            attack='100',
            max_life=300,
            description='monster description',
        ),
    )

@pytest.fixture
def example_five_items():
    lst = []
    for i in range(5):
        lst.append(Items.objects.create(name='Item' + str(i), description='Item' + str(i) + 'description',
                                        bonuses_to_life=10 * i, slug='item-' + str(i), modification_to_attack=i))
        return lst

@pytest.fixture
def example_five_abilities():
    lst = []
    for i in range(5):
        lst.append(Abilities.objects.create(name='Skill' + str(i), description='Skill' + str(i) + 'description',
                                            damage=i + 1, slug='Skill' + str(i), heal=i + 1, modification='mod' + str(i)))
        return lst

@pytest.fixture
def example_enemy():
    return Enemies.objects.create(
        name='Enemy 1',
        life=2000,
        attack='100',
        max_life=2000,
        current_life=2000,
        description='monster description',
        type=1,
    )

def example_BOOS():
    return Enemies.objects.create(
        name='Boss',
        life=3000,
        attack='300',
        max_life=3000,
        current_life=2000,
        description='monster description',
        type=1,
    )