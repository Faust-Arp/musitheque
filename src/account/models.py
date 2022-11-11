from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Vous devez renseigner un nom d'utilisateur")

        user = self.model()
        user.username=username
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)

        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        unique=True,
        max_length=255,
        blank=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


