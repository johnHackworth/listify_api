from datetime import datetime
import json

class lfyModel():
  fields = []
  def asDict(self, fields = None):
    if fields is None:
      fields = self.fields
    dictionary = {}
    for field in fields:
      fieldValue = getattr(self,field)
      if type(fieldValue) is datetime:
        print field
        fieldValue = unicode(fieldValue)

      dictionary[field] = fieldValue
    return dictionary

  def asJSON(self, fields = None):
    return json.dumps(self.asDict(fields))