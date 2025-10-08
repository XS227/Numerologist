from django.urls import path

from .views import intake_view

app_name = "intake"

urlpatterns = [
    path("", intake_view, name="form"),
]
