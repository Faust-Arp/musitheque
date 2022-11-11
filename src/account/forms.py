from django.contrib.auth.forms import UserCreationForm

from account.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', ]
