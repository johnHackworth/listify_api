class lfyException(Exception):
	txt = 'error: '
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.txt+str(self.value))


class MethodNotAllowedException(lfyException):
	txt = 'Method not allowed: '

class InvalidFieldsException(lfyException):
	txt = 'Some fields are invalid: '

class InvalidPasswordException(lfyException):
	txt = 'Invalid password: '

class ExistingUserException(lfyException):
	txt = 'Invalid user: '

class ExistingEmailException(ExistingUserException):
	txt = 'Existing email: '

class ExistingLoginException(ExistingUserException):
	txt = 'Existing login: '	