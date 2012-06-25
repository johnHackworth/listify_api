from users.models import Passwordchange, User
from crypt import crypt
from django.conf import settings

class Password_recovery_service_mock():

    password_change = None
    return_value = True

    def create(self, user_id):
        password_recovery_request = Passwordchange(user_id=user_id)
        self.password_change = password_recovery_request
        return password_recovery_request

    def check_hash(self, hash, user_id):
        if self.return_value == False:
            return None
        if self.password_change is None:
            self.create(user_id)
        self.password_change.hash = hash
        return self.password_change

    def mark_hash_as_used(self, user_id):
        self.password_change.used = True

class UsersTestCaseFactory:
    def user(self):
        user = User()
        user.name = 'Johnathan Percival'
        user.lastname = 'Hackworth'
        user.login = 'theAlchemist'
        user.password = crypt("abcde", settings.PASSWORD_SALT)
        user.email = 'thealchemis@listify.es'
        user.location = 'Shangai'
        user.country = 1
        user.gender = 1
        user.aboutme = 'Nanotechnology and neovictorianism'
        return user

    def users(self):
        user = User()
        user.name = 'Erasmas'
        user.login = 'erasmas'
        user.password = crypt("abcde", settings.PASSWORD_SALT)
        user.email = 'a1@listify.es'
        user.save()
        user2 = User()
        user2.name = 'Orolo'
        user2.login = 'orolo'
        user2.password = crypt("abcde", settings.PASSWORD_SALT)
        user2.email = 'a2@listify.es'

        user2.save()
        user3 = User()
        user3.name = 'Raz'
        user3.login = 'raz'
        user3.password = crypt("abcde", settings.PASSWORD_SALT)
        user3.email = 'a3@listify.es'

        user3.save()
        return [user, user2, user3]
