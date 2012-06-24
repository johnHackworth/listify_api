from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from users.user_service import User_service
from users.models import User, UserList
from users.session_service import Session_service
from users.password_recovery_service import Password_recovery_service
from friends.friendship_service import Friendship_service
from commons.exceptions import InvalidFieldsException, InvalidPasswordException, ExistingUserException, TooMuchAttempsException
from commons.models import lfyHandler


class SessionHandler(lfyHandler):
    allowed_methods = ('GET')
    user_service = User_service()
    session_service = Session_service(user_service)

    def read(self, request):

        login = request.GET.get('username')
        password = request.GET.get('password')
        result = self.session_service.logUser(login, password)
        if result is None:
            return HttpResponseNotFound('<h1>Login or password incorrect</h1>')
        else:
            return HttpResponse(result)

    def delete(self, id, request):
        # delete session
        pass


class UserHandler(lfyHandler):

    allowed_methods = ('GET, POST, PUT, DELETE')
    user_service = User_service()
    session_service = Session_service(user_service)
    fields = ["name", "lastname", "email", "location", "country", "gender", "aboutme", "languaje"]

    def getUser(self, value, field):
        user = self.user_service.findUser({field: value})
        if user is not None:
            return HttpResponse(user.asJSON())
        else:
            return HttpResponseNotFound('<h1>User not found</h1>')

    def read(self, request, identification):
        if identification.isdigit():
            return self.getUser(identification, "id")
        else:
            return self.getUser(identification, "login")

    def update(self, request, identification):
        sessionDTO = self.getSessionData(request)
        loggedUser = self.session_service.getLoggedUser(sessionDTO)
        if loggedUser is not None:
            if str(loggedUser.id) != str(identification):
                return HttpResponseForbidden('<h1>not the user</h1>')
            else:
                self.fromRequest(request, loggedUser, self.fields)
                try:
                    loggedUser = self.user_service.saveUser(loggedUser)
                except InvalidFieldsException as invalid_fields:
                    return HttpResponseForbidden(invalid_fields)
                except ExistingUserException as invalid_user:
                    return HttpResponseForbidden(invalid_user)
                return HttpResponse(loggedUser.asJSON())
        else:
            return HttpResponseForbidden('<h1>not a user</h1>')

    def create(self, request):
        user = User()
        self.fromRequest(request, user, self.fields)
        user.login = request.POST.get('login')
        try:
            self.user_service.assignPassword(user, None, request.POST.get('password'))
        except InvalidPasswordException as invalid_password:
            return HttpResponseForbidden(invalid_password)
        try:
            user = self.user_service.saveUser(user)
        except InvalidFieldsException as invalid_fields:
            return HttpResponseForbidden(invalid_fields)
        except ExistingUserException as invalid_user:
            return HttpResponseForbidden(invalid_user)

        return HttpResponse(user.asJSON())


class FriendsHandler(lfyHandler):

    allowed_methods = ('GET')
    user_service = User_service(Friendship_service())
    fields = ["id", "login", "name", "lastname", "email", "location", "country", "gender", "aboutme", "languaje"]

    def read(self, request, identification):
        user = self.user_service.findUser({"id": identification})
        friends = UserList(self.user_service.getFriendsList(user))

        return HttpResponse(friends.asJSON(self.fields))


class PasswordChangeHandler(lfyHandler):

    allowed_methods = ('PUT, POST')
    user_service = User_service(Friendship_service())
    password_request_service = Password_recovery_service()

    def create(self, request):
        user_email = request.POST.get('user_email')
        user = self.user_service.findUser({"email": user_email})
        if user is not None:
            try:
                self.password_request_service.create(user.id)
                return HttpResponse()
            except TooMuchAttempsException:
                return HttpResponseForbidden('You have requested a new password too much. Wait some time.')
        else:
            return HttpResponseForbidden('User not found')

    def update(self, request):
        hash = request.PUT.get('hash')
        new_password = request.PUT.get('password')
        user_email = request.PUT.get('email')

        user = self.user_service.findUser({"email": user_email})
        if user is not None:
            if self.user_service.changePassword(user, hash, new_password):
                return HttpResponse()
            else:
                return HttpResponseNotFound('Incorrect hash')
        else:
            return HttpResponseForbidden('invalid user')





