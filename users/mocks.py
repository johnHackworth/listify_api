from users.models import Passwordchange


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
