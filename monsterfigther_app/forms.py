import django.forms as forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from monsterfigther_app.models import PlayerMonster

# Form to login to a game
class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='Login')
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Password')

# validation if username is already taken
def validate_login_name(value):
    if User.objects.filter(username=value):
        raise ValidationError('Login is already taken')

# registration for new players whit validation for password
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, label='Login', validators=[validate_login_name])
    pass1 = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Password')
    pass2 = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Confirm password')
    email = forms.EmailField(max_length=128, label='Enter email')
    first_name = forms.CharField(max_length=128, label='First name')
    last_name = forms.CharField(max_length=128, label='Last name')
    stage = forms.IntegerField(widget=forms.HiddenInput, initial=1)

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data['pass1']
        pass2 = cleaned_data['pass2']
        if pass1 != pass2:
            raise ValidationError('Passwords are different')
        return cleaned_data

# for to resset a pass for a logged player
class ResetPasswordIfLoggedForm(forms.Form):
    new_pass1 = forms.CharField(max_length=128, label='New password', widget=forms.PasswordInput)
    new_pass2 = forms.CharField(max_length=128, label='Confirm new password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_pass1 = cleaned_data['new_pass1']
        new_pass2 = cleaned_data['new_pass2']
        if new_pass1 != new_pass2:
            raise ValidationError('Passwords are different')
        return cleaned_data

# Checking if name of monster already exist
def validation_for_player_monster_name(value):
    if PlayerMonster.objects.filter(name=value):
        raise ValidationError('This name is already taken')

# Form to create monster
class CreatePlayerMonsterForm(forms.Form):
    name = forms.CharField(max_length=64, label='Choose a name for Your monster',
                           validators=[validation_for_player_monster_name])
    monster = forms.ModelChoiceField(queryset=PlayerMonster.objects.filter(id__lte=3), widget=forms.Select)

#Form to change items wearing by monster, max three items
class UpdateMonsterItemsForm(forms.ModelForm):
    class Meta:
        model = PlayerMonster
        fields = ['equip_slot']

    def clean(self):
        cleaned_data = super().clean()
        equip_slot = cleaned_data['equip_slot']
        if len(equip_slot) > 3:
            raise ValidationError('Choose max three items')
        return cleaned_data

#Form to change skill that monster can use, max three items
class UpdateMonsterSkillsForm(forms.ModelForm):
    class Meta:
        model = PlayerMonster
        fields = ['special_player_attack']

    def clean(self):
        cleaned_data = super().clean()
        player_attack = cleaned_data['special_player_attack']
        if len(player_attack) > 3:
            raise ValidationError('Choose max three abilities')
        return cleaned_data

# Skill Attack  1 Form
class Attack1ButtonForm(forms.Form):
    attack = forms.IntegerField(required=False, widget=forms.HiddenInput)
    heal = forms.IntegerField(required=False, widget=forms.HiddenInput)

# Skill Attack  2 Form
class Attack2ButtonForm(forms.Form):
    attack = forms.IntegerField(required=False, widget=forms.HiddenInput)
    heal = forms.IntegerField(required=False, widget=forms.HiddenInput)

# Skill Attack  3 Form
class Attack3ButtonForm(forms.Form):
    attack = forms.IntegerField(required=False, widget=forms.HiddenInput)
    heal = forms.IntegerField(required=False, widget=forms.HiddenInput)

#Form whit Yest to select to star new game
class NewGameForm(forms.Form):
    YES = forms.BooleanField(required=False, initial=False)

