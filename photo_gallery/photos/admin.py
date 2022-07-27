import copy
from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    fields = ['large_image', 'thumbnail_img_tag']
    list_display = ('__str__', 'thumbnail_img_tag')

    # Display a non-editable thumbnail on Photo change pages
    readonly_fields = ['thumbnail_img_tag']

    def get_fields(self, request, obj=None):
        """Return a list of fields (str) for the Photo add form (obj=None) or change form.
        https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_fields
        https://github.com/django/django/blob/stable/4.0.x/django/contrib/admin/options.py#L365
        """
        if obj is None:
            # Prevent modification of any lists within `fields`
            add_fields = copy.deepcopy(self.fields)
            # Don't display (non-existent) thumbnail on "add" view
            add_fields.remove('thumbnail_img_tag')
            return add_fields

        return super().get_fields(request, obj)


admin.site.register(Photo, PhotoAdmin)
