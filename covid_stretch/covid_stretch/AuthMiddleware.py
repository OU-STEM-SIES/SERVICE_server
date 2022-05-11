# AuthMiddleware.py
# Based on code found at https://stackoverflow.com/questions/62024580/how-can-i-authenticate-a-user-with-a-query-parameter-on-any-url

# my_project/authentication_backends.py
from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.middleware import AuthenticationMiddleware

TOKEN_QUERY_PARAM = "token"

class TokenMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        try:
            token = request.GET[TOKEN_QUERY_PARAM]
            print ("--- URL token parameter was: '" + str(token) + "'.")
        except KeyError:
            # A token isn't included in the query params
            return

        if request.user.is_authenticated:
            # Here you can check that the authenticated user has the same `token` value
            # as the one in the request. Otherwise, logout the already authenticated
            # user.
            if request.user.token.key == token:
                return
            else:
                auth.logout(request)

        user = auth.authenticate(request, token=token)
        if user:
            print("--- User token is: '" + str(request.user.token.key) + "'.")
            # The token is valid. Save the user to the request and session.
            request.user = user
            auth.login(request, user)

class TokenBackend(ModelBackend):
    def authenticate(self, request, token=None):
        if not token:
            return None

        try:
            return User.objects.get(token__key=token)
            print("--- User token is: '" + str(request.user.token.key) + "'.")
        except User.DoesNotExist:
            # A user with that token does not exist
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
