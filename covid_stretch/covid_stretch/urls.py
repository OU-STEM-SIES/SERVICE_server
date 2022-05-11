from . import views

from django.contrib import admin
# from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from user_profile.views import UserProfileViewSet, UserViewSet, CoSViewSet, UserLogViewSet
from moods.views import MoodViewSet, PagedMoodsList
# from messaging.views import MessageViewSet
# from emotional_status.views import EmotionViewSet
# from . import views
from .views import CustomObtainAuthToken, CustomLogout  # , LogoutWebView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename='Users')
router.register(r"profile", UserProfileViewSet, basename='UserProfile')
router.register(r"cos", CoSViewSet, basename='CirclesOfSupport')
router.register(r"log", UserLogViewSet, basename='UserLog')
router.register(r"moods", MoodViewSet, basename='Moods')
# router.register(r"emotions", EmotionViewSet, basename='Emotional_status')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # path('logoutweb/', LogoutWebView, name='logoutweb'),
    # path("logoutapi/", LogoutView.as_view(), name="logoutapi"),
    # path("", include(router.urls)),
    path("", include("dashboard.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("api/", include("user_profile.urls")),
    path("api/", include(router.urls)),
    path("api/pagedmoods/", PagedMoodsList.as_view(), name="pagedmoodslist"),

    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("api-auth/", ObtainAuthToken.as_view()),
    # url(r'^authenticate/', CustomObtainAuthToken.as_view()),
    path("api-auth/", CustomObtainAuthToken.as_view()),
    path("logoutapi/", CustomLogout.as_view()),  #, name="auth_logout"),
    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
