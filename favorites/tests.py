from django.test import TestCase
from commons.exceptions import NotLoggedException
from favorites.models import *
from favorites.mocks import FavoritesTestCaseFactory
from favorites.favorites_service import Favorites_service
from users.session_service import *
from users.mocks import UsersTestCaseFactory
from users.user_service import *
from items.mocks import ItemTestCaseFactory
from django.utils.unittest import skipIf


class FavoritesSeviceTest(TestCase):
    cases_factory = FavoritesTestCaseFactory()
    item_factory = ItemTestCaseFactory()
    user_service = User_service()
    session_service = Session_service(user_service)
    favorites_service = Favorites_service(session_service)
    user_factory = UsersTestCaseFactory()

    mock_user = None

    def create_mock_session(self):
        user = self.user_factory.user()
        user.save()
        self.mock_user = user
        return self.session_service.createSession(user.id)

    def test_create_favorite(self):
        session_DTO = self.create_mock_session()

        fav = self.favorites_service.create(session_DTO.get_session_DTO(), 1)

        self.assertEquals(fav.user_id, session_DTO.user_id)
        self.assertEquals(fav.item_id, 1)

    def test_create_existing_favorite(self):
        session_DTO = self.create_mock_session()

        fav = self.favorites_service.create(session_DTO.get_session_DTO(), 2)
        fav2 = self.favorites_service.create(session_DTO.get_session_DTO(), 2)

        self.assertEquals(fav.id, fav2.id)

    def test_delete_favorite(self):
        session_DTO = self.create_mock_session()
        fav = self.favorites_service.create(session_DTO.get_session_DTO(), 3)

        self.favorites_service.delete(session_DTO.get_session_DTO(), 3)

        persisted = Favorite.objects.filter(user_id=session_DTO.user_id, item_id=3)

        self.assertEquals(len(persisted), 0)

    def test_unlogged_delete(self):
        session_DTO = self.create_mock_session()
        fav = self.favorites_service.create(session_DTO.get_session_DTO(), 4)

        another_session_DTO = self.create_mock_session()
        session_DTO.user_id = another_session_DTO.user_id

        try:
            self.favorites_service.delete(session_DTO.get_session_DTO(), 4)
            self.fail('It let you delete favorites for a not logged user')
        except NotLoggedException:
            self.assertTrue(True)

    @skipIf(True, True)
    def test_get_user_favorites(self):
        item1 = self.item_factory.item()
        item2 = self.item_factory.item()
        item3 = self.item_factory.item()
        fav = self.favorites_service.create(4, item1.id)
        fav2 = self.favorites_service.create(4, item2.id)
        fav3 = self.favorites_service.create(4, item3.id)

        favorites = self.favorites_service.get_user_favorites(4)

        self.assertEquals(len(favorites), 3)

        self.assertEquals(favorites[0].id, item1.id)
        self.assertEquals(favorites[1].id, item2.id)
        self.assertEquals(favorites[2].id, item3.id)

    @skipIf(True, True)
    def test_get_user_favorited(self):
        item1 = self.item_factory.item()
        item1.user_id = 4
        item1.save()
        item2 = self.item_factory.item()
        item2.user_id = 4
        item2.save()
        item3 = self.item_factory.item()
        item3.user_id = 4
        item3.save()
        fav = self.favorites_service.create(5, item1.id)
        fav2 = self.favorites_service.create(6, item2.id)
        fav3 = self.favorites_service.create(7, item3.id)

        favorited = self.favorites_service.get_user_favorited(1)

        self.assertEquals(len(favorited), 3)

        self.assertEquals(favorited[0].id, item1.id)
        self.assertEquals(favorited[1].id, item2.id)
        self.assertEquals(favorited[2].id, item3.id)







