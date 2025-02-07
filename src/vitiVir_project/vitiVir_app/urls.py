from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .views import UserViewSet, LoginViewSet, BlastViewSet, ContactView, RequestAccountView, GetDBStatsView

router= routers.DefaultRouter()
router.register('users/manageusers', UserViewSet)
router.register('users/login', LoginViewSet, basename='login')
router.register('api/blast', BlastViewSet, basename='blast')

urlpatterns = [
    path('', include(router.urls)),
    path('api/blast/', BlastViewSet.as_view({'post': 'post'})),
    path('api/contact/', ContactView.as_view()),
    path('api/request_account/', RequestAccountView.as_view()),
    path('stats/', GetDBStatsView.as_view()),
]