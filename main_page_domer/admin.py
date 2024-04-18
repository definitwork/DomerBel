from django.contrib import admin

from main_page_domer.models import Complaint, ReasonOfComplaint, Publication, Comment, PhotoPublication


class PublicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Complaint)
admin.site.register(ReasonOfComplaint)
admin.site.register(PhotoPublication)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Comment)
