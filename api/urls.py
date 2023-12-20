from django.urls import path,include
from home.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'peoples', PeopleViewSet, basename='peoples')
urlpatterns = router.urls


urlpatterns = [
  path('index/', index),
  path('people/', people),
  path('login/', login),
  path('persons/', PersonAPI.as_view()),
  path('register/', ResgisterAPI.as_view()),
  path('', include(router.urls))
]