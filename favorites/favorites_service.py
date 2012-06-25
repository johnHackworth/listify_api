from favorites.models import *
from commons.exceptions import NotLoggedException


class Favorites_service():

    session_service = None

    def __init__(self, session_service = None):
        self.session_service = session_service

    def create(self, session_DTO, item_id):
        user = self.session_service.getLoggedUser(session_DTO)
        if user is None:
            raise NotLoggedException
        else:
            favorite = Favorite.objects.filter(user_id=user.id, item_id=item_id)
            if len(favorite) == 0:
                favorite = Favorite(user_id=user.id, item_id=item_id)
                favorite.save()
            else:
                favorite = favorite[0]

            return favorite

    def delete(self, session_DTO, item_id):
        user = self.session_service.getLoggedUser(session_DTO)
        if user is None:
            raise NotLoggedException
        else:
            favorites = Favorite.objects.filter(user_id=user.id, item_id=item_id)
            for fav in favorites:
                fav.delete()
            return None

    def get_user_favorites(self, user_id):
        pass

    def get_user_favorited(self, user_id):
        pass
