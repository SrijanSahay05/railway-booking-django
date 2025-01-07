from django.contrib import admin
from .models import Station, Train, SeatCategory, Route, HaltStation


# Register your models here.
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(SeatCategory)
admin.site.register(HaltStation)
admin.site.register(Route)
