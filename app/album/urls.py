from django.urls import path, include
from rest_framework.routers import DefaultRouter

from album import views

router = DefaultRouter()  # new object
router.register('albums', views.AlbumViewSet)

app_name = 'album'

urlpatterns = [
    path('', include(router.urls))
]
