from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id').first()
        except ObjectDoesNotExist:
            return None
        if user.check_password(password):
            print(user)
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None