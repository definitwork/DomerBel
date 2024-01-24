from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from advertisement.models import Advertisement, Complaint, ReasonOfComplaint, Category, Region, Gallery, Photo, \
    Publication, Comment, FieldSet, Field, Spisok, Element, ElementTwo, Store


# Register your models here.

class AdvertisementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class RegionAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("area",)}


class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PublicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Complaint)
admin.site.register(ReasonOfComplaint)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Comment)
admin.site.register(FieldSet)
admin.site.register(Field)
admin.site.register(Spisok)
admin.site.register(Element)
admin.site.register(ElementTwo)
admin.site.register(Store, StoreAdmin)
