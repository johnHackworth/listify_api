class List_service_mock():

    list = None

    def findOneList(self, filter):
        return self.list

    def mocked_list(self):
        mocked_list = {
            "permissions": 0,
            "name": "test",
            "user_id": 0
        }
        self.list = mocked_list
        return self.list
