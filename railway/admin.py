from django.contrib import admin
from .models import Station, TrainSegment, SeatCategory, Seat,  Route, HaltStation, RouteHaltSegments, Train

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city')
    search_fields = ('name', 'code', 'city')

class TrainSegmentAdmin(admin.ModelAdmin):
    list_display = ('halt_segment', 'date')
    search_fields = ('halt_segment__route__name', 'date__date')
    list_filter = ('date', 'halt_segment__route')

class SeatCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'seat_fare')
    search_fields = ('name', 'code')

class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'source', 'destination', 'departure_time', 'arrival_time', 'duration', 'base_fare')
    search_fields = ('name', 'number', 'source__name', 'destination__name')
    list_filter = ('source', 'destination', 'running_days')

class HaltStationAdmin(admin.ModelAdmin):
    list_display = ('station', 'route', 'arrival_time', 'departure_time', 'order')
    search_fields = ('station__name', 'route__name')
    list_filter = ('route', 'station')

class RouteHaltSegmentsAdmin(admin.ModelAdmin):
    list_display = ('route', 'current_halt', 'previous_halt', 'segment_number')
    search_fields = ('route__name', 'current_halt__name', 'previous_halt__name')
    list_filter = ('route', 'current_halt', 'previous_halt')

# Register your models here.
admin.site.register(Station, StationAdmin)
admin.site.register(TrainSegment, TrainSegmentAdmin)
admin.site.register(SeatCategory, SeatCategoryAdmin)
admin.site.register(HaltStation, HaltStationAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteHaltSegments, RouteHaltSegmentsAdmin)
admin.site.register(Train)  
admin.site.register(Seat)
