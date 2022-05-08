from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import AdvUser, Equipment, Category, Subcategory, Brand, Post, Comment, Store, Characteristic, City, \
    Region, Delivery, Payment, Wishes, EquipmentStatistic

admin.site.register(AdvUser)



admin.site.register(Brand)


admin.site.register(Characteristic)

admin.site.register(City)
admin.site.register(Region)
admin.site.register(Payment)
admin.site.register(Delivery)
admin.site.register(Wishes)
admin.site.register(EquipmentStatistic)




class EquipmentAdmin(TranslationAdmin):
    list_display = ('title', 'brand', 'available', 'price', 'remainder', 'description', 'subcategory', 'image',
                    'characteristic', 'discount',)

admin.site.register(Equipment, EquipmentAdmin)

# ----------------------------------------------------------------------------------------------------------------------


class PostAdmin(TranslationAdmin):
    list_display = ('title', 'slug', 'user', 'short_description', 'content', 'created_on')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)


# ----------------------------------------------------------------------------------------------------------------------


class CategoryAdmin(TranslationAdmin):
    list_display = ('title', )

admin.site.register(Category, CategoryAdmin)


# ----------------------------------------------------------------------------------------------------------------------


class SubcategoryAdmin(TranslationAdmin):
    list_display = ('title', 'category',)

admin.site.register(Subcategory, SubcategoryAdmin)


# ----------------------------------------------------------------------------------------------------------------------


class StoreAdmin(TranslationAdmin):
    list_display = ('title',)

admin.site.register(Store, StoreAdmin)


# ----------------------------------------------------------------------------------------------------------------------







