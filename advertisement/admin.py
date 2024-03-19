from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from advertisement.models import Advertisement,  Category, Region, PhotoAdvertisement, \
     FieldSet, Field, Spisok, Element, ElementTwo


# Register your models here.

class AdvertisementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class RegionAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("area",)}


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(PhotoAdvertisement)
admin.site.register(FieldSet)
admin.site.register(Field)
admin.site.register(Spisok)
admin.site.register(Element)
admin.site.register(ElementTwo)

