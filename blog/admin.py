from django.contrib import admin
from .models import Post, Day
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

# Register your models here.
# admin.site.register(Post)
admin.site.register(Day)


class PostAdmin(admin.ModelAdmin):
    list_filter = (
        ('day__number', DropdownFilter),
    )

    list_display = ['title', 'get_email', 'day', 'anything_else']

    search_fields = ['title', 'author__username', 'author__email', 'author__first_name', 'author__last_name']

    def get_email(self, obj):
        return obj.author.email
    get_email.admin_order_field  = 'email' 
    get_email.short_description = 'Email' 

admin.site.register(Post, PostAdmin)