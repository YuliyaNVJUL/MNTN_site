from modeltranslation.translator import register, TranslationOptions
from .models import Equipment, Characteristic, Category, Subcategory, Store, Post, Comment


@register(Equipment)
class EquipmentTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'available', )


@register(Characteristic)
class CharacteristicTranslationOptions(TranslationOptions):
    fields = ('appointment', 'level',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'category',)

@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'slug', 'short_description', 'content',)



