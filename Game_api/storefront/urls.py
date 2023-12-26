from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from storefront.views import test
from storefront.views import Game_type_all
from storefront.views import make_and_modal_data


urlpatterns = [
    path('sf/', test),
    path('sfd/', Game_type_all),
    path('make/', make_and_modal_data),
]
