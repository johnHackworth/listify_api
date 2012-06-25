from friends.models import Friendship


class Friendship_service():

    def getFriendshipById(self, user_id, friend_id):
        friendship = Friendship.objects.filter(user_id=user_id, friend_id=friend_id)
        return friendship

    def getFriendship(self, user, friend):
        return self.getFriendshipById(user.id, friend.id)

    def isFriendById(self, user_id, friend_id):
        if user_id == friend_id:
            return True
        friendship = self.getFriendshipById(user_id, friend_id)
        if len(friendship) > 0:
            return True
        else:
            return False

    def isFriend(self, user, friend):
        return self.isFriendById(user.id, friend.id)

    def getRelationById(self, user_id, friend_id):
        if user_id == friend_id:
            return Friendship.SAME_USER
        elif self.isFriendById(user_id, friend_id):
            return Friendship.FRIENDS
        else:
            return Friendship.STRANGERS

    def getRelation(self, user, friend):
        return self.getRelationById(user.id, friend.id)


    def makeFriendship(self, user, friend):
        if self.getRelation(user, friend) == Friendship.STRANGERS:
            friendship = Friendship()
            friendship.user_id = user.id
            friendship.friend_id = friend.id
            friendship.save()
        return True

    def removeFriendship(self, user, friend):
        friendships = self.getFriendship(user, friend)
        for friendship in friendships:
            friendship.delete()
        return True

    def getUserFriendsIds(self, user):
        friendships = Friendship.objects.filter(user_id=user.id)
        friend_ids = []
        for friendship in friendships:
            friend_ids.append(friendship.friend_id)
        return friend_ids
