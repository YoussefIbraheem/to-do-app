from django.contrib import admin
from .models import ToDo, Category

class ToDoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status')
    search_fields = ('title',)
    ordering = ('title',)
    
    
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(ToDo, ToDoAdmin)
