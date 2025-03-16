from django.contrib import admin

# Register your models here.
from website.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_date'
admin.site.register(Contact, ContactAdmin)

from website.models import Newsletter

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
admin.site.register(Newsletter, NewsletterAdmin)

