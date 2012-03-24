"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from users.models import *
from users.user_service import *
from users.session_service import *

class testCaseFactory:
	def user(self):
		user = User()
		user.name = 'Johnathan Percival'
		user.lastname = 'Hackworth'
		user.login = 'theAlchemist'
		user.password = crypt.crypt("abcde", settings.PASSWORD_SALT)
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
		user.save()
		user2 = User()
		user2.name = 'Orolo'
		user2.login = 'orolo'
		user2.save()
		user3 = User()
		user3.name = 'Raz'
		user3.login = 'raz'
		user3.save()
		return [user, user2, user3]

class UserModelTest(TestCase):
	casesFactory = testCaseFactory()

	def test_export_dictionary(self):
		user = self.casesFactory.user()

		dictObj = user.asDict(['name','lastname','country'])
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

class userServiceTest(TestCase):
	casesFactory = testCaseFactory()
	user_service = User_service()

	def test_find_user(self):
		newUsers = self.casesFactory.users()

		user1 = self.user_service.findUser({"name" : "Orolo"})
		
		self.assertEquals(user1.name, "Orolo")
		self.assertEquals(user1.login, "orolo")

		user2 = self.user_service.findUser({"login" : 'erasmas'})
		self.assertEquals(user2.name, "Erasmas")
		self.assertEquals(user2.login, "erasmas")

		user3 = self.user_service.findUser({"login" : 'Fra'})
		self.assertEquals(user3, None)

	def test_log_user(self):
		user = self.casesFactory.user()
		user.save()

		session = self.user_service.logUser('theAlchemist', 'abcde');

		self.assertFalse(session == None);

		# add some json checks

class sessionServiceTest(TestCase):
	casesFactory = testCaseFactory()
	user_service = User_service()	
	session_service = Session_service()

	def test_create_session(self):
		session = self.session_service.createSession(1)
		self.assertTrue(session.user_id == 1)
		self.assertTrue(session.hash is not None)
		self.assertTrue(len(session.hash) > 10)

	def test_check_session(self):
		session = self.session_service.createSession(1)
		session.save()

		sessionExists = self.session_service.checkSession(1,session.id, session.hash)

		self.assertTrue(sessionExists)



