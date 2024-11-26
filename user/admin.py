from django.contrib import admin
from .models import Request, Category

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'user']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'user__username']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

