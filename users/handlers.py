from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from users.user_service import User_service
from users.models import User, UserList
from users.session_service import Session_service
from friends.friendship_service import Friendship_service
from commons.exceptions import InvalidFieldsException, InvalidPasswordException, ExistingUserException
from commons.models import lfyHandler


class LoginHandler(lfyHandler):
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
        loggedUser = self.session_service.getLoggedUser(request)
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
