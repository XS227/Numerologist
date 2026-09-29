from django.urls import path

from . import views

app_name = "members"

urlpatterns = [
    path("min-side/login/", views.member_login, name="login"),
    path("min-side/logout/", views.member_logout, name="logout"),
    path("min-side/", views.dashboard, name="dashboard"),
    path("min-side/rapport/<str:order_id>/", views.report_view, name="report"),
    path("konto/google/", views.google_start, name="google_start"),
    path("konto/google/callback/", views.google_callback, name="google_callback"),
    path("konto/vipps/", views.vipps_start, name="vipps_start"),
    path("konto/vipps/callback/", views.vipps_callback, name="vipps_callback"),
    path("konto/vipps/broker/", views.vipps_broker_handoff, name="vipps_broker_handoff"),
    path("konto/vipps/complete/", views.vipps_complete, name="vipps_complete"),
    path("academy/", views.academy, name="academy"),
    path("academy/niva/<int:level>/", views.academy_level, name="academy_level"),
    path("academy/premium/<int:level>/<slug:resource_slug>/", views.premium_resource, name="premium_resource"),
    path("rapporter/demo/<slug:package_slug>/", views.report_demo, name="report_demo"),
]
