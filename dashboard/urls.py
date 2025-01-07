from django.urls import path
from . import views as dashboard_views

urlpatterns = [
    path("", dashboard_views.index, name="index"),
    path("search-trains/", dashboard_views.SearchTrains, name="search_trains"),
    path("profile/", dashboard_views.profile, name="profile"),
    path("passenger-profile/", dashboard_views.PassengerProfilePage, name="passenger_profile"),
    path("staff-profile/", dashboard_views.StaffProfilePage, name="staff_profile"),
]
