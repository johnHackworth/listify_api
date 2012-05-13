from django.test import TestCase
from friends.models import *
from friends.friendship_service import *
from users.tests import usersTestCaseFactory


class FriendshipModelTest(TestCase):
    casesFactory = usersTestCaseFactory()

    def test_create(self):
        user1 = self.casesFactory.user()
        friend = self.casesFactory.user()

        fr = Friendship(user1.id, friend.id)

        self.assertEquals(fr.user_id, user1.id)
        self.assertEquals(fr.friend_id, friend.id)


class FriendshipServiceTest(TestCase):
    casesFactory = usersTestCaseFactory()
    friendship_service = Frienship_service(None)

    user1 = self.casesFactory.user()
    friend = self.casesFactory.user()


    def test_findOneItem(self):
        friendship = Friendship(self.user1.id, self.friend.id)

        friendshipPersisted= self.item_service.findOneItem({"user_id":self.user1.id})
        self.assertEquals(friendshipPersistedd.user_id, self.user1.id)

