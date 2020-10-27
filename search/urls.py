from django.urls import path,include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'request', views.RequestModelViewset)
router.register(r'history', views.DonationHistoryView)
urlpatterns = [
    path('search/',views.SearchView.as_view()),
    path('',include(router.urls)),
]