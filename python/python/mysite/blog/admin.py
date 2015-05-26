from django.contrib import admin
from blog.models import *

# Register your models here.

class Blog_admin(admin.ModelAdmin):
	list_display=('title','summary','view_count','created_at','category_name')
	list_filter=('created_at',)
	search_fields=('title','summary','category_name__name')

admin.site.register(Blog,Blog_admin)
admin.site.register(Category)