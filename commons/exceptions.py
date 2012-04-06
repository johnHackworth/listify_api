class MethodNotAllowed(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		txt = 'Method not allowed: '
		return repr(txt+self.value)

class InvalidFields(Exception):
	def __init__(self, fields):
		self.fields = fields
	def __str__(self):
		txt = 'Some fields are invalid: '+str(self.fields)
		return repr(txt)