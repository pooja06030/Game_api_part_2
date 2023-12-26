from django.contrib import admin
from django.contrib import admin
from storefront.models import store_frant
from storefront.models import category
from storefront.models import Storemap
from storefront.models import storefrontcategoryMapping
from storefront.models import Make_and_Models
from storefront.models import make_and_Models_mapping
# Register your models here.


class Make_and_ModelsAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'active']


admin.site.register(Make_and_Models, Make_and_ModelsAdmin)


class make_and_Models_mappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'Make_and_modle', 'Game']


admin.site.register(make_and_Models_mapping, make_and_Models_mappingAdmin)


class store_frantAdmin(admin.ModelAdmin):
    list_display = ['Game', 'device', 'category']


admin.site.register(store_frant, store_frantAdmin)


class StorefrontCategoryMappingInline(admin.TabularInline):
    model = storefrontcategoryMapping
    extra = 1  # category empty he to ye show hoga


class Storemap_Admin(admin.ModelAdmin):
    inlines = [StorefrontCategoryMappingInline]
    list_display = ['Game', 'game_category',   'device',
                    'Game_type',  'is_active', 'create_at', 'update_at']

    def game_category(self, obj):
        cat_list = []
        cat_name = ""
        for cat in obj.sfcategory.all():
            cat_list.append(cat.category.category_name)
            if cat_list:
                cat_name = ",".join(cat_list)
        return cat_name


admin.site.register(Storemap,  Storemap_Admin)


class category_Admin(admin.ModelAdmin):
    # inlines = [StorefrontCategoryMappingInline]
    list_display = ['id', 'category_name', 'category_description', 'category_image',
                    'category_icon_upload', 'category_icon_url', 'active', 'category_subtitle', 'notes']


admin.site.register(category, category_Admin)


# class  storefrontcategoryMapping_Admin(admin.ModelAdmin):
#      list_display = ['id', 'storemap','category','is_active','create_at','update_at']

# admin.site.register( storefrontcategoryMapping,  storefrontcategoryMapping_Admin)

############################################################################################

# Register your models here.
