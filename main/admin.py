from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customusers,categorie,product,cart,Payment


class CustomUserAdmin(UserAdmin):
    model = Customusers()
    fieldsets = UserAdmin.fieldsets + (
      ('Extra Fields', {'fields':
       ('atype',
       'earning',
       'name')}),
     )
admin.site.register(Customusers, CustomUserAdmin)
admin.site.register(categorie)
admin.site.register(product)
admin.site.register(cart)
admin.site.register(Payment)
