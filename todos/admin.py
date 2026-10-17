from django.contrib import admin
from .models import ToDO
# Register your models here.

@admin.register(ToDO)
class ToDOAdmin(admin.ModelAdmin):
    list_display = ('title','completed','created_at','description')
    list_filter = ('completed',)
    search_fields = ('title','description')


