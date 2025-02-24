from django.contrib import admin

# Register your models here.
from website.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_date'
admin.site.register(Contact, ContactAdmin)