from django.test import TestCase
from commons.exceptions import NotLoggedException
from favorites.models import *
from favorites.mocks import FavoritesTestCaseFactory
from favorites.favorites_service import Favorites_service
from users.session_service import *
from users.mocks import UsersTestCaseFactory
from users.user_service import *
from items.mocks import ItemTestCaseFactory
from items.item_service import Item_service
from friends.friendship_service import Friendship_service
from lists.list_service import List_service
from lists.models import List
from django.utils.unittest import skipIf


class FavoritesSeviceTest(TestCase):
    cases_factory = FavoritesTestCaseFactory()
    item_factory = ItemTestCaseFactory()
    user_service = User_service()
    session_service = Session_service(user_service)
    friendship_service = Friendship_service()
    list_service = List_service(None)
    item_service = Item_service(list_service, friendship_service, user_service)
    favorites_service = Favorites_service(session_service, friendship_service, item_service)
    user_factory = UsersTestCaseFactory()

    mock_user = None

    def create_mock_session(self):
        user = self.user_factory.user()
        user.save()
        self.mock_user = user
        session = self.session_service.createSession(user.id)
        return session.get_session_DTO()

    def test_create_favorite(self):
        session_DTO = self.create_mock_session()
        item1 = self.item_factory.persited_item()

        fav = self.favorites_service.create(session_DTO, item1.id)

        self.assertEquals(fav.user.id, session_DTO["user_id"])
        self.assertEquals(fav.item.id, 1)

    def test_create_existing_favorite(self):
        session_DTO = self.create_mock_session()
        item1 = self.item_factory.persited_item()

        fav = self.favorites_service.create(session_DTO, item1.id)
        fav2 = self.favorites_service.create(session_DTO, item1.id)

        self.assertEquals(fav.id, fav2.id)


    def test_delete_favorite(self):
        session_DTO = self.create_mock_session()
        item = self.item_factory.persited_item()

        fav = self.favorites_service.create(session_DTO, item.id)
        user = self.user_service.find(id=session_DTO["user_id"])

        self.favorites_service.delete(session_DTO, item.id)

        persisted = Favorite.objects.filter(user=user, item=item)

        self.assertEquals(len(persisted), 0)


    def test_unlogged_delete(self):
        session_DTO = self.create_mock_session()
        item = self.item_factory.persited_item()
        fav = self.favorites_service.create(session_DTO, item.id)

        another_session_DTO = self.create_mock_session()
        session_DTO["user_id"] = another_session_DTO["user_id"]

        try:
            self.favorites_service.delete(session_DTO, item.id)
            self.fail('It let you delete favorites for a not logged user')
        except NotLoggedException:
            self.assertTrue(True)

    def test_get_user_favorites(self):
        test_list = List(user_id=10, name="test", permissions=0)
        test_list.save()
        item1 = self.item_factory.persited_item()
        item1.list_id = test_list.id
        item1.save()

        item2 = self.item_factory.persited_item()
        item2.list_id = test_list.id
        item2.save()

        session_DTO = self.create_mock_session()
        user = self.user_service.find(id=session_DTO["user_id"])

        fav = self.favorites_service.create(session_DTO, item1.id)
        fav2 = self.favorites_service.create(session_DTO, item2.id)

        item_favorites = self.favorites_service.get_user_favorites(session_DTO, user)

        self.assertEquals(len(item_favorites), 2)

        self.assertEquals(item_favorites[0].id, item1.id)
        self.assertEquals(item_favorites[1].id, item2.id)

    def test_get_item_favorites(self):
        test_list = List(user_id=10, name="test", permissions=0)
        test_list.save()

        session_DTO = self.create_mock_session()

        item1 = self.item_factory.item()
        item1.user_id = session_DTO["user_id"]
        item1.list_id = test_list.id
        item1.save()

        fav = self.favorites_service.create(session_DTO, item1.id)

        item_favorites = self.favorites_service.get_item_favorites(session_DTO, item1.id)

        self.assertEquals(len(item_favorites),1)
        self.assertEquals(item_favorites[0].id, fav.id)


    def test_get_user_favorited(self):
        test_list = List(user_id=10, name="test", permissions=0)
        test_list.save()

        session_DTO = self.create_mock_session()

        item1 = self.item_factory.item()
        item1.user_id = session_DTO["user_id"]
        item1.list_id = test_list.id
        item1.save()

        item2 = self.item_factory.item()
        item2.user_id = session_DTO["user_id"]
        item2.list_id = test_list.id
        item2.save()

        session_DTO2 = self.create_mock_session()
        fav = self.favorites_service.create(session_DTO2, item1.id)
        session_DTO3 = self.create_mock_session()
        fav2 = self.favorites_service.create(session_DTO3, item2.id)

        user = self.user_service.find(id=session_DTO["user_id"])
        favorited = self.favorites_service.get_user_favorited(session_DTO, user)

        self.assertEquals(len(favorited), 2)

        self.assertEquals(favorited[0]["item_id"], item1.id)
        self.assertEquals(favorited[1]["item_id"], item2.id)






