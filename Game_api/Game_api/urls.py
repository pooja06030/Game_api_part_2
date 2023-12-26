from django.contrib import admin
from django.urls import path, include
from Game_app import views
from rest_framework.routers import DefaultRouter
from storefront.views import test
from Game_app.views import register_user
from Game_app.views import verify_otp
from Game_app.views import login_user
from Game_app.views import  send_otp_via_email
from storefront.views import Game_type_all
from storefront.views import make_and_modal_data
from django.conf import settings


router = DefaultRouter()


router.register('GameMakerapi', views.GameMakerSerializerViewSet,
                basename='GameMaker')
router.register('Developerapi', views.DeveloperSerializerViewSet,
                basename='Developer')
router.register('Game_Developer_api',
                views.Developer_games_SerializerViewSet, basename='Game_Developer')


#  path('approved/<int:pk>', views.approved, name='approved'),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('storefront/', include('storefront.urls')),
    path('register/',  register_user),
    path('login/',  login_user),
    path('email/',  send_otp_via_email),
    path('verify/',  verify_otp),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
