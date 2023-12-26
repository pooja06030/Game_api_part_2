from django.contrib import admin
from django.contrib import admin
from Game_app.models import Developer
from Game_app.models import GameMaker
from Game_app.models import GameMaker
from Game_app.models import device_frant
from storefront.models import category
from Game_app.models import custom_user
from Game_app.models import User
from django.contrib.sessions.models import Session

# from jio_app.models import store_frant
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_verified',
                    'otp']

admin.site.register(User, UserAdmin)    




class GameMakerAdmin(admin.ModelAdmin):
    list_display = ['game_name', 'game_type', 'game_price',
                    'is_active', 'include_ads', 'developer', 'device']


admin.site.register(GameMaker, GameMakerAdmin)


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'address', 'create_at', 'update_at']


admin.site.register(Developer, DeveloperAdmin)


class device_frant_Admin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(device_frant, device_frant_Admin)


class custom_userAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'password']


admin.site.register(custom_user, custom_userAdmin)

# Register your models here.
