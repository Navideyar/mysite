from django.contrib import admin
from blog.models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.



class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ["title", "author" , "counted_views", "status", "login_required" ,"published_date" , "created_date" ]
    list_filter = ["author", "status", "created_date", "updated_date"]
    search_fields = ["title", "content", "author__username"]
    summernote_fields = ('content',)
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "approved", "created_date", "updated_date"]
    list_filter = ["approved", "created_date", "updated_date"]
    search_fields = ["name", "subject", "message"]
    list_editable = ["approved"]
    empty_value_display = "-empty-"
    date_hierarchy = "created_date"
    
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
