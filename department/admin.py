from django.contrib import admin

# Register your models here.

from .models import Department, Consumer

admin.site.register(Department)
admin.site.register(Consumer)
