from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from users.user_service import User_service
from friends.friendship_service import Friendship_service
from friends.models import Friendship
from commons.models import lfyHandler


class FriendshipHandler(lfyHandler):
    friendship_service = Friendship_service()
    user_service = User_service()

    def read(self, request, user_id, friend_id):

        user1 = self.user_service.findUser({"id": user_id})
        user2 = self.user_service.findUser({"id": friend_id})

        if user1 is not None and user2 is not None:
            relation = self.friendship_service.getRelation(user1, user2)
            if relation != Friendship.STRANGERS:
                return HttpResponse('Ok')
            else:
                return HttpResponse(status=204)
        else:
            return HttpResponseNotFound('No user found')

    def create(self, request, user_id, friend_id):
        user1 = self.user_service.findUser({"id": user_id})
        user2 = self.user_service.findUser({"id": friend_id})

        if user1 is not None and user2 is not None:
            try:
                self.friendship_service.makeFriendship(user1, user2)
                return HttpResponse('Ok')
            except:
                return HttpResponseServerError('error making the friendship')
        else:
            return HttpResponseNotFound('No user found')

    def delete(self, request, user_id, friend_id):
        user1 = self.user_service.findUser({"id": user_id})
        user2 = self.user_service.findUser({"id": friend_id})

        if user1 is not None and user2 is not None:
            try:
                self.friendship_service.removeFriendship(user1, user2)
                return HttpResponse('Ok')
            except:
                return HttpResponseServerError('error deleting the friendship')
        else:
            return HttpResponseNotFound('No user found')
