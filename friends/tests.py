from django.test import TestCase
from friends.models import *
from friends.friendship_service import Friendship_service
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
    friendship_service = Friendship_service()

    def createUsers(self):
        self.user1 = self.casesFactory.user()
        self.friend = self.casesFactory.user()
        self.user1.save()
        self.friend.save()

    def deleteUsers(self):
        self.user1.delete()
        self.friend.delete()

    def test_findOneFriendship(self):
        self.createUsers()
        friendship = Friendship()
        friendship.user_id = self.user1.id
        friendship.friend_id = self.friend.id
        friendship.save()

        friendshipPersisted = self.friendship_service.getFriendship(self.user1, self.friend)
        self.assertEquals(friendshipPersisted[0].user_id, self.user1.id)



    def test_makeFriendship(self):
        self.createUsers()

        friendship = self.friendship_service.makeFriendship(self.user1, self.friend)
        friendshipPersisted = self.friendship_service.getFriendship(self.user1, self.friend)

        self.assertTrue(friendship)
        self.assertTrue(friendshipPersisted[0].id)
        self.assertEquals(friendshipPersisted[0].user_id, self.user1.id)
        self.assertEquals(friendshipPersisted[0].friend_id, self.friend.id)
        self.deleteUsers()

    def test_deleteFriendship(self):
        self.createUsers()

        self.friendship_service.makeFriendship(self.user1, self.friend)
        friendshipDeleted = self.friendship_service.removeFriendship(self.user1, self.friend)
        friendshipPersisted = self.friendship_service.getFriendship(self.user1, self.friend)

        self.assertTrue(friendshipDeleted)
        self.assertFalse(friendshipPersisted)

        self.deleteUsers()

    def test_areFriends(self):
        self.createUsers()

        self.friendship_service.makeFriendship(self.user1, self.friend)
        friends = self.friendship_service.isFriend(self.user1, self.friend)
        self.assertTrue(friends)

        friends = self.friendship_service.isFriend(self.user1, self.user1)
        self.assertTrue(friends)

        self.friendship_service.removeFriendship(self.user1, self.friend)
        friends = self.friendship_service.isFriend(self.user1, self.friend)
        self.assertFalse(friends)

        self.deleteUsers()

    def test_getRelation(self):
        self.createUsers()

        self.friendship_service.makeFriendship(self.user1, self.friend)

        relation = self.friendship_service.getRelation(self.user1, self.friend)
        self.assertEquals(relation, Friendship.FRIENDS)

        relation = self.friendship_service.getRelation(self.user1, self.user1)
        self.assertEquals(relation, Friendship.SAME_USER)

        self.friendship_service.removeFriendship(self.user1, self.friend)
        relation = self.friendship_service.getRelation(self.user1, self.friend)
        self.assertEquals(relation, Friendship.STRANGERS)

        self.deleteUsers()

    def test_getFriendsIds(self):
        self.createUsers()

        self.friendship_service.makeFriendship(self.user1, self.friend)

        friend_ids = self.friendship_service.getUserFriendsIds(self.user1)

        self.assertEquals(friend_ids, [self.friend.id])

        self.deleteUsers()
