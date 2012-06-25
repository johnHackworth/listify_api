from django.db import models
from commons.models import lfyModel


class Favorite(lfyModel, models.Model):
    class Meta:
        db_table = 'favorites'

    user_id = models.IntegerField(max_length=11)
    item_id = models.IntegerField(max_length=11)
    models.DateField(auto_now=True, auto_now_add=True)

