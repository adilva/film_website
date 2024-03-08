from django.contrib import admin
from . models import category,products,User
admin.site.register(User)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
admin.site.unregister(get_user_model())

class categoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(category,categoryAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ['name','category_id','actors']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20
admin.site.register(products,productAdmin)