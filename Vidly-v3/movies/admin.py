from django.contrib import admin
from .models import Genre,Movie
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):list_display=['id','name']
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=['title','genre','total_quantity','number_in_stock','daily_rate','active']
    search_fields=['title','barcode']
    list_filter=['active','genre']
    readonly_fields=['total_quantity','number_in_stock']
    def has_add_permission(self,request):return False
    def has_delete_permission(self,request,obj=None):return False
