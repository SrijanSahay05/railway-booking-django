from django.urls import path
from . import views as railway_views

urlpatterns = [
    path("add-train/", railway_views.AddTrain, name="add_train"),
]