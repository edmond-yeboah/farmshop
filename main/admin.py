from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customusers,categorie,product


class CustomUserAdmin(UserAdmin):
    model = Customusers()
    fieldsets = UserAdmin.fieldsets + (
      ('Extra Fields', {'fields':
       ('atype',
       'name')}),
     )
admin.site.register(Customusers, CustomUserAdmin)
admin.site.register(categorie)
admin.site.register(product)
