from friends.models import Friendship


class Friendship_service():

    def getFriendship(self, user, friend):
        friendship = Friendship.objects.filter(user_id=user.id, friend_id=friend.id)
        return friendship

    def isFriend(self, user, friend):
        if user.id == friend.id:
            return True
        friendship = self.getFriendship(user, friend)
        if len(friendship) > 0:
            return True
        else:
            return False

    def getRelation(self, user, friend):
        if user.id == friend.id:
            return Friendship.SAME_USER
        elif self.isFriend(user, friend):
            return Friendship.FRIENDS
        else:
            return Friendship.STRANGERS

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
