from django.contrib.auth.models import User,Group
from DataBase_MPMS.models import Users as SystemUser
from ..Services.UserService import UserService
from django.contrib.auth.backends import ModelBackend
import logging

LOGGER = logging.getLogger(__name__)

class UserBackend(ModelBackend):

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            # Try to find a user matching your username
            #  Check the password is the reverse of the username
            check_status = UserService.check_user(username, password)
            if check_status['status']:
                user = User(username=username)
                user.pk = check_status['data']['inc_id']
                user.is_staff = True
                user.is_superuser = check_status['data']['issuper'] and check_status['data']['issuper'] == 1
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except Exception as e:
            # No user was found, return None - triggers default login failed
            LOGGER.error(e)
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            system_user = SystemUser.objects.get(pk=user_id)
            user = User(username=system_user.username)
            user.pk = system_user.inc_id
            user.is_staff = True
            user.is_superuser = system_user.issuper and system_user.issuper == 1
            return user
        except Exception as e:
            LOGGER.error(e)
            return None