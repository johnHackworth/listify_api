from users.models import User
from commons.exceptions import InvalidPasswordException, InvalidFieldsException, ExistingEmailException, ExistingLoginException
from django.conf import settings
import crypt
import json


class User_service():

    friendship_service = None
    password_recovery_service = None

    def __init__(self, friendship_service=None, password_recovery_service=None):
        self.friendship_service = friendship_service
        self.password_recovery_service = password_recovery_service

    def findUser(self, filter):
        users = User.objects.filter(**filter)
        if len(users) > 0:
            return users[0]
        else:
            return None

    def userSessionInfo(self, user, session):
        userDict = user.asDict()
        userDict['session'] = session.asDict(["id", "hash"])
        return json.dumps(userDict)

    def saveUser(self, user):
        try:
            user.validate()
        except InvalidFieldsException as invalidFields:
            raise invalidFields

        sameEmailUsers = User.objects.filter(email=user.email)
        for sameEmailUser in sameEmailUsers:
            if user.id != sameEmailUser.id:
                raise ExistingEmailException(user.email)

        sameLoginUsers = User.objects.filter(login=user.login)
        for sameLoginUser in sameLoginUsers:
            if user.id != sameLoginUser.id:
                raise ExistingLoginException(user.login)

        user.save()
        return user

    def assignPassword(self, user, old_password, new_password):
        if user.id is None or user.password == crypt.crypt(old_password, settings.PASSWORD_SALT):
            user.password = crypt.crypt(new_password, settings.PASSWORD_SALT)
            return user
        else:
            raise InvalidPasswordException(old_password)

    def getFriendsList(self, user):
        friends_ids = self.friendship_service.getUserFriendsIds(user)

        friends = []

        for friend_id in friends_ids:
            user = self.findUser({"id": friend_id})
            if user is not None:
                friends.append(user)

        return friends

    def changePassword(self, user, hash, password):
        if self.password_recovery_service is not None:
            change_password = self.password_recovery_service.check_hash(hash, user.id)
            if change_password is not None:
                user.password = crypt.crypt(password, settings.PASSWORD_SALT)
                user.save()
                self.password_recovery_service.mark_hash_as_used(user.id)
                return True
            else:
                return False
        return False


