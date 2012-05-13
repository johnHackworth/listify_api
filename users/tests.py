"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from users.models import *
from users.user_service import User_service
from users.session_service import *
from friends.friendship_service import Friendship_service
from commons.mocks import RequestFactory
from crypt import crypt
from commons.exceptions import InvalidFieldsException, InvalidPasswordException
import json


class usersTestCaseFactory:
    def user(self):
        user = User()
        user.name = 'Johnathan Percival'
        user.lastname = 'Hackworth'
        user.login = 'theAlchemist'
        user.password = crypt("abcde", settings.PASSWORD_SALT)
        user.email = 'thealchemist@listify.es'
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


class UserModelTest(TestCase):
    casesFactory = usersTestCaseFactory()

    def test_export_dictionary(self):
        user = self.casesFactory.user()

        dictObj = user.asDict(['name', 'lastname', 'country'])
        self.assertEqual(dictObj['name'], 'Johnathan Percival')
        self.assertEqual(dictObj['lastname'], 'Hackworth')
        self.assertEqual(dictObj['country'], 1)
        try:
            gender = dictObj['gender']
            self.assertFalse(True)
        except:
            self.assertTrue(True)

        dictObj = user.asDict(['gender'])
        try:
            country = dictObj['country']
            self.assertFalse(True)
        except:
            self.assertTrue(True)
        self.assertTrue(dictObj['gender'] == 1)

    def test_export_json(self):
        user = self.casesFactory.user()
        jsonObj = user.asJSON(['name'])
        print jsonObj
        self.assertTrue(jsonObj =='{"name": "Johnathan Percival"}')

    def test_validate(self):
        user = self.casesFactory.user()
        user.login = None
        user.password = None
        user.email = None
        try:
            user.validate()
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)
        except:
            self.fail('bad type of exception')

        user.login = 'a'
        try:
            user.validate()
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)
        except:
            self.fail('bad type of exception')

        user.password = 'a'
        try:
            user.validate()
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)
        except:
            self.fail('bad type of exception')

        user.email = 'a'
        try:
            user.validate()

        except:
            self.fail()







class userServiceTest(TestCase):
    casesFactory = usersTestCaseFactory()
    user_service = User_service(None, Friendship_service())
    session_service = Session_service(user_service)

    def test_findUser(self):
        newUsers = self.casesFactory.users()

        user1 = self.user_service.findUser({"name" : "Orolo"})

        self.assertEquals(user1.name, "Orolo")
        self.assertEquals(user1.login, "orolo")

        user2 = self.user_service.findUser({"login" : 'erasmas'})
        self.assertEquals(user2.name, "Erasmas")
        self.assertEquals(user2.login, "erasmas")

        user3 = self.user_service.findUser({"login" : 'Fra'})
        self.assertEquals(user3, None)


    def test_saveUser(self):
        user = User()
        try:
            self.user_service.saveUser(user)
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)

        user.login = 'prueba'
        user.password = 'prueba'
        user.email = 'prueba@prueba'

        try:
            user = self.user_service.saveUser(user)
        except InvalidFieldsException:
            self.fail()

        userDB = self.user_service.findUser({'login':'prueba'})

        self.assertEquals(user.id, userDB.id)

    def test_saveRepeatedUser(self):

        user = User()
        user.login = 'prueba'
        user.password = 'prueba'
        user.email = 'prueba@prueba'
        try:
            self.user_service.saveUser(user)
        except:
            self.fail()

        user2 = User()
        user2.login = 'prueba'
        user2.password = 'prueba'
        user2.email = 'prueba2@prueba'
        success = False
        try:
            self.user_service.saveUser(user2)
        except:
            success = True
        self.assertTrue(success)

        user3 = User()
        user3.login = 'prueba3'
        user3.password = 'prueba'
        user3.email = 'prueba@prueba'
        success = False
        try:
            self.user_service.saveUser(user3)
        except:
            success = True
        self.assertTrue(success)

    def test_userSessionInfo(self):
        newUsers = self.casesFactory.users()
        user1 = self.user_service.findUser({"name" : "Orolo"})
        session = self.session_service.createSession(user1.id)

        userSessionInfo = self.user_service.userSessionInfo(user1, session)

        testCase = user1.asDict()
        testCase2 = session.asDict(["id", "hash"])
        testCase["session"] = testCase2
        testCase = json.dumps(testCase)



        self.assertEquals(testCase, userSessionInfo)

    def test_assignPassword(self):

        newUsers = self.casesFactory.users()
        user1 = self.user_service.findUser({"name" : "Orolo"})

        success = False
        try:
            self.user_service.assignPassword(user1, 'prueba', 'prueba2')
        except InvalidPasswordException:
            success = True
        except:
            success = False
        self.assertTrue(success)

        try:
            self.user_service.assignPassword(user1, 'abcde', 'prueba2')
            success = True
        except:
            success = False

        self.assertTrue(success)

    def test_getFriendsList(self):
        self.casesFactory.users()
        user1 = self.user_service.findUser({"name": "Orolo"})
        user2 = self.user_service.findUser({"name": "Erasmas"})
        user3 = self.user_service.findUser({"name": "Raz"})
        self.user_service.friendship_service.makeFriendship(user1, user2)
        self.user_service.friendship_service.makeFriendship(user1, user3)

        friends = self.user_service.getFriendsList(user1)

        self.assertEquals(len(friends), 2)
        self.assertEquals(friends[0].id, user2.id)
        self.assertEquals(friends[1].id, user3.id)






class sessionServiceTest(TestCase):
    casesFactory = usersTestCaseFactory()
    user_service = User_service()
    session_service = Session_service(user_service)

    def test_create_session(self):
        session = self.session_service.createSession(1)
        self.assertTrue(session.user_id == 1)
        self.assertTrue(session.hash is not None)
        self.assertTrue(len(session.hash) > 10)

    def test_getSession(self):
        session = self.session_service.createSession(1)
        session.save()
        rf = RequestFactory()
        request = rf.get('fake/path')
        request = rf.setHeaders(1,session.id, session.hash, request)

        userSession = self.session_service.getSession(request)
        self.assertFalse(userSession is None)
        self.assertTrue(userSession.id == session.id)
        self.assertTrue(userSession.user_id == 1)


    def test_logUser(self):
        user = self.casesFactory.user()
        user.save()

        session = self.session_service.logUser('theAlchemist', 'abcde');

        self.assertFalse(session == None);

    def test_getLoggedUser(self):
        user = self.casesFactory.user()
        user.save()
        session = self.session_service.createSession(user.id)
        session.save()

        rf = RequestFactory()
        request = rf.get('fake/path')
        request = rf.setHeaders(user.id,session.id, session.hash, request)

        loggedUser = self.session_service.getLoggedUser(request)

        self.assertFalse(loggedUser is None)
        self.assertEquals(user.id, loggedUser.id)





