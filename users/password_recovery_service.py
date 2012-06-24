from users.models import Passwordchange
from commons.exceptions import TooMuchAttempsException
from datetime import datetime, timedelta


class Password_recovery_service():

    def create(self, user_id):
        lastHourDateTime = datetime.today() - timedelta(hours=1)
        previous_requests = Passwordchange.objects.filter(
            user_id=user_id, used=False, date__gt=lastHourDateTime)
        if len(previous_requests) >= 5:
            raise TooMuchAttempsException(len(previous_requests))

        password_recovery_request = Passwordchange(user_id=user_id)
        password_recovery_request.save()

        return password_recovery_request

    def check_hash(self, hash, user_id):
        requests = Passwordchange.objects.filter(hash=hash, user_id=user_id, used=False)
        persisted = None
        if len(requests) != 0:
            newer_requests = Passwordchange.objects.filter(
                hash=hash, user_id=user_id, date__gt=requests[0].date)
            if len(newer_requests) == 0:
                persisted = requests[0]

        return persisted

    def mark_hash_as_used(self, user_id):
        requests = Passwordchange.objects.filter(user_id=user_id)
        for r in requests:
            r.used = True
            r.save()

