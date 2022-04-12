from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


TYPE_OF_MONSTER = (
    (1, 'Enemy'),
    (2, 'BOSS'),
    (3, 'ENDBOSS'),
)
'''
Simple game, that player choose a monster and fight against enemy,
by using a set of abilities and items.
'''

# abstract model to create a PlayerMonster, Enemies
class Monster(models.Model):
    name = models.CharField(max_length=64, unique=True)
    life = models.PositiveIntegerField(null=False)
    attack = models.PositiveIntegerField(null=False)
    description = models.TextField(null=True)
    current_life = models.IntegerField(null=True, default=1)
    max_life = models.PositiveIntegerField(null=True, default=1)

    class Meta:
        abstract = True


# model of available items to use by Your monster during game
class Items(models.Model):
    name = models.CharField(max_length=64, unique=True)
    bonuses_to_life = models.IntegerField(null=True)
    description = models.TextField(null=True)
    modification_to_attack = models.IntegerField(null=True)
    slug = models.SlugField(max_length=64, default="automatically")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Items, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Monster that player will use to fight
class PlayerMonster(Monster):
    equip_slot = models.ManyToManyField(Items, default=None, null=True)
    special_player_attack = models.ManyToManyField('Abilities', default=None, null=True)

    def __str__(self):
        return self.name

# model of enemies whit inheritance model form Monster and simple choice of type of enemie
class Enemies(Monster):
    type = models.IntegerField(choices=TYPE_OF_MONSTER, null=False)

    def __str__(self):
        return self.name

# skill that player monster can use
class Abilities(models.Model):
    name = models.CharField(unique=True, max_length=64)
    damage = models.PositiveIntegerField(null=True)
    heal = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    modification = models.CharField(max_length=64, null=True)
    slug = models.SlugField(max_length=64, default='automatically')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Abilities, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


'''
Player whit inheritance from User model, whit two extra fields - player_items and current_stage,
and m2m field to PlayerMonster
'''
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player_items = models.ManyToManyField(Items, default=None, null=True)
    current_stage = models.PositiveIntegerField(null=False, default=1)
    player_monster = models.ForeignKey(PlayerMonster, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.user.username
