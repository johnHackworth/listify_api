from favorites.models import *


class FavoritesTestCaseFactory:
    def favorite(self):
        fav = Favorite()
        fav.user_id = 1
        fav.item_id = 1
        return fav
