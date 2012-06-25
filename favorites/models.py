from django.db import models
from commons.models import lfyModel
from users.models import User
from items.models import Item

class Favorite(lfyModel, models.Model):
    class Meta:
        db_table = 'favorites'

    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    models.DateField(auto_now=True, auto_now_add=True)

