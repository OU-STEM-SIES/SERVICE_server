# from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
from user_profile import views

# router = routers.DefaultRouter()
# router.register(r"profile", views.UserProfileViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path("", include(router.urls)),
#     path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
# ]

urlpatterns = [
    path('add_user', views.RegisterNewUser.as_view()),
    path('add_supporter', views.add_supporter, name='add_supporter'),
    path('edit_supporter', views.edit_supporter, name='edit_supporter'),
    path('remove_supporter', views.remove_supporter, name='remove_supporter'),
    ]
