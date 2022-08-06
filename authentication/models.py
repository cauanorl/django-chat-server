from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AllFriendsManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs
        return qs


class Friend(models.Model):
    # O usuário que enviar a solicitação
    user_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend_one",
        blank=True,
        null=True)
    # O usuário que receberá a solicitação
    user_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friend_two",
        blank=True,
        null=True)

    # Se a solicitação foi aceita
    accept = models.BooleanField(null=True, blank=True)

    objects = models.Manager()

    def get_friend(self, user):
        match user:
            case self.user_one:
                return self.user_two
            case self.user_two:
                return self.user_one
            case _:
                return None

    def __str__(self) -> str:
        return f"{self.user_one} and {self.user_two}; status: {self.accept}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # A lista de amigos
    friends = models.ManyToManyField(Friend, blank=True, db_index=True)

    def __str__(self):
        return f"{self.user} profile"
