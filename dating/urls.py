from django.urls import path
from . import views

app_name = "dating"
urlpatterns = [
    path("", views.experiment, name="home"),
    path("profile/", views.edit_profile, name="profile"),
    path("matches/", views.matches, name="matches"),
    path("connection/<int:pk>/", views.connection, name="connection"),
    path("delete/", views.delete_profile, name="delete"),
]
