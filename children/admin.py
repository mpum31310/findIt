from django.contrib import admin
from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'grade', 'school', 'parent', 'created_at')
    list_filter = ('grade', 'school', 'created_at')
    search_fields = ('name', 'surname', 'school')

