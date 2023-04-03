from django.contrib import admin
from .models import UserProfile
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
import csv
from django.http import HttpResponse


# Register your models here.
# admin.site.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ['blocked', ('date_blocked', DropdownFilter),]

    list_display = ['first_name', 'last_name','user', 'get_email', 'acount_id']

    actions = ['export_as_csv']

    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'acount_id']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

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
            userprofile = obj
            user = userprofile.user
            instagram = userprofile.insta_handler
            website = userprofile.url
            email_address = user.email
            first_name = user.first_name
            last_name = user.last_name
            row = writer.writerow([ first_name, last_name, email_address, instagram, website])
        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(UserProfile, UserProfileAdmin)