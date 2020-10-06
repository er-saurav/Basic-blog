from django.contrib import admin
from .models import UserProfile, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','status','created_on')
    list_filter = ('status',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug':('title',)}

admin.site.register(UserProfile)
admin.site.register(Post)
# Register your models here.
