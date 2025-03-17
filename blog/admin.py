from django.contrib import admin
from blog.models import Post, Category
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.



class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["title", "author" , "counted_views", "status", "published_date" , "created_date" ]
    list_filter = ["author", "status", "created_date", "updated_date"]
    search_fields = ["title", "content", "author__username"]
    summernote_fields = ('content',)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)