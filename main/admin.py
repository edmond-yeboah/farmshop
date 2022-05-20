from django.contrib import admin
from .models import ToDoList
from .models import Farmer
from .models import Customer
from .models import Product
from .models import Order


from django.contrib.auth.admin import UserAdmin
from .models import Customusers


# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Farmer)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)


class CustomUserAdmin(UserAdmin):
    model = Customusers()
    fieldsets = UserAdmin.fieldsets + (
      ('Extra Fields', {'fields':
       ('atype',
       'name')}),
     )
admin.site.register(Customusers, CustomUserAdmin)
