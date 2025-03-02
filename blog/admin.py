from django.contrib import admin
from blog.models import Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    fields = ["image","author", "title", "content", "status"]
    list_display = ["title", "author" , "status", "created_date", "updated_date", "counted_views"]
    list_filter = ["author", "status", "created_date", "updated_date"]
    search_fields = ["title", "content", "author__username"]
