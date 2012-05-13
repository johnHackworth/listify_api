from django.db import models
from commons.models import lfyModel


class Friendship(lfyModel, models.Model):

    SAME_USER = 2
    FRIENDS = 1
    STRANGERS = 0

    levels = [SAME_USER, FRIENDS, STRANGERS]

    user_id = models.IntegerField(max_length=11)
    friend_id = models.IntegerField(max_length=11)

  # alter table users_friendship rename friends_friendship