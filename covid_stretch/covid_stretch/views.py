# from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from rest_framework import status
# from rest_framework import authentication, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.serializers import UserSerializer

# from django.http import HttpResponse

# from django.http import Http404, HttpResponse, JsonResponse
# from django.shortcuts import redirect, render
# from django.contrib.auth.models import User
# from moods.models import Moods
# from user_profile.models import Linkworker, Person_at_centre, Supporter, UserProfile


# def LogoutWebView(request):
#     logout(request)
#     # Redirect to a success page.
#     return HttpResponse("Successfully logged out. Goodbye. <a href='/'>Log back in?</a>")

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        responsedata = {
            'token': token.key,
            # 'id': token.user_id,
            }

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # user = serializer.object.get('user') or request.user
            user = User.objects.get(pk=token.user_id)
            # responsedata['user'] = UserSerializer(user).data
            responsedata.update(UserSerializer(user).data)
            pass
        return Response(responsedata)


class CustomLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        # request.user.auth_token.delete()
        Token.objects.get(user=request.user).delete()
        return Response(
                {"response": "Successfully logged out."},
                status=status.HTTP_200_OK
                )


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in. See https://www.bedjango.com/blog/top-6-django-decorators/ """

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)
# The way to use this decorator is:
#     @group_required("admins", "seller")
#     def my_view(request, pk)
#         ...

#
# class ExampleView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         content = {
#             'user': str(request.user),  # `django.contrib.auth.User` instance.
#             'auth': str(request.auth),  # None
#         }
#         return Response(content)
#
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes((IsAuthenticated,))
# def example_view(request, format=None):
#     content = {
#         'user': str(request.user),  # `django.contrib.auth.User` instance.
#         'auth': str(request.auth),  # None
#     }
#     return Response(content)
