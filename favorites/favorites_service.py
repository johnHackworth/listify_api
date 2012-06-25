from favorites.models import *
from commons.exceptions import NotLoggedException, InvalidFieldsException
from django.db.models import Q
import operator

class Favorites_service():

    session_service = None
    friendship_service = None
    item_service = None

    def __init__(self, session_service=None, friendship_service=None, item_service=None):
        self.session_service = session_service
        self.friendship_service = friendship_service
        self.item_service = item_service

    def create(self, session_DTO, item_id):
        user = self.session_service.getLoggedUser(session_DTO)
        item = self.item_service.find(id=item_id)

        if user is None:
            raise NotLoggedException
        elif item is None:
            raise InvalidFieldsException
        else:
            favorite = Favorite.objects.filter(user=user, item=item)
            if len(favorite) == 0:
                favorite = Favorite(user=user, item=item)
                favorite.save()
            else:
                favorite = favorite[0]

            return favorite

    def delete(self, session_DTO, item_id):
        user = self.session_service.getLoggedUser(session_DTO)
        item = self.item_service.find(id=item_id)

        if user is None:
            raise NotLoggedException
        elif item is None:
            raise InvalidFieldsException
        else:
            favorites = Favorite.objects.filter(user=user, item=item)
            for fav in favorites:
                fav.delete()
            return None

    def get_user_favorites(self, session_DTO, user):
        logged_user = self.session_service.getLoggedUser(session_DTO)

        favorites = Favorite.objects.filter(user=user)
        filtered_favorites = []

        for fav in favorites:
            fav_item = self.item_service.findOne({"id": fav.item.id})
            if self.item_service.is_viewable(fav_item, logged_user.id):
                filtered_favorites.append(fav_item)

        return filtered_favorites

    def get_item_favorites(self, session_DTO, item_id):
        logged_user = self.session_service.getLoggedUser(session_DTO)

        item = self.item_service.find(id=item_id)
        if self.item_service.is_viewable(item, logged_user.id):
            favorites = Favorite.objects.filter(item=item).select_related()
            return favorites
        else:
            return []

    def get_user_favorited(self, session_DTO, user):
        logged_user = self.session_service.getLoggedUser(session_DTO)

        items = self.item_service.findItems({"user_id": user.id})

        condition = reduce(operator.or_, [Q(item=i) for i in items])
        favorites = Favorite.objects.filter(condition).select_related()

        filtered = {}

        for fav in favorites:
            if self.item_service.is_viewable(fav.item, logged_user.id):
                if fav.id not in filtered:
                    filtered[fav.id] = []

                user_dict = {
                    "login": fav.user.login,
                    "id": fav.user.id
                }
                item_dict = {
                    "user": user_dict,
                    "item_id": fav.item.id
                }

                filtered[fav.id] = item_dict

        items = []
        for f in filtered:
            items.append(filtered[f])

        return items
