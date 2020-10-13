from django.contrib import admin
from main.models import Aliment, Category, Substitute

class AlimentAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'nutrition_grades')

admin.site.register(Aliment, AlimentAdmin)
admin.site.register(Category)
admin.site.register(Substitute)
