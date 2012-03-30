from django.db import models
import json

class lfyModel():
  fields = []
  def asDict(self, fields = None):
    if fields is None:
      fields = self.fields
    dictionary = {}
    for field in fields:
      dictionary[field] = getattr(self,field)
    return dictionary

  def asJSON(self, fields = None):
    return json.dumps(self.asDict(fields))