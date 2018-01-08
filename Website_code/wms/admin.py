from django.contrib import admin
from .models import Plant,waterTank,location
# Register your models here.

admin.site.register(Plant)
admin.site.register(waterTank)
admin.site.register(location)
