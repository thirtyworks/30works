from django.contrib import admin
from .models import Post, Day
from users.models import UserProfile
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
import csv
from django.http import HttpResponse

# Register your models here.
# admin.site.register(Post)
admin.site.register(Day)


class PostAdmin(admin.ModelAdmin):
    list_filter = (
        ('day__number', DropdownFilter),
    )

    list_display = ['title', 'get_email', 'day', 'anything_else']

    search_fields = ['title', 'author__username', 'author__email', 'author__first_name', 'author__last_name']
    
    actions = ['export_as_csv']

    def get_email(self, obj):
        return obj.author.email
    get_email.admin_order_field  = 'email' 
    get_email.short_description = 'Email' 

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        # writer.writerow(field_names+['email'])
        # for obj in queryset:
        #     userprofile = obj
        #     user = userprofile.user
        #     email_address = user.email
        #     print('email = {}'.format(email_address))
        #     row = writer.writerow([getattr(obj, field) for field in field_names] + [email_address, first_name])
        
        # limited fields
        writer.writerow(['first_name', 'last_name','email', 'instagram', 'website'])
        for obj in queryset:
            user = obj.author
            userprofile = UserProfile.objects.get(user=user)
            instagram = userprofile.insta_handler
            website = userprofile.url
            email_address = user.email
            first_name = user.first_name
            last_name = user.last_name
            row = writer.writerow([ first_name, last_name, email_address, instagram, website])
        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(Post, PostAdmin)