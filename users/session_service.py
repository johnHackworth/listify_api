from users.models import Session
from django.conf import settings
import crypt, random

class Session_service():

  def createSession(self, user_id):
    session = Session()
    session.user_id = user_id
    session.hash = crypt.crypt(str(random.random()), settings.SESSION_SALT)+crypt.crypt(str(random.random()), settings.SESSION_SALT)
    return session

  def checkSession(self, user_id, session_id, session_hash):
  	result = Session.objects.filter(user_id = user_id, id = session_id, hash = session_hash)
  	if len(result) == 0:
  		return False
  	else:
  		return True
