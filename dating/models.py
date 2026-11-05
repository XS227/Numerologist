from django.conf import settings
from django.db import models


class DatingProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Calculation inputs are private; only alias, city and age appear in matches.
    full_name = models.CharField(max_length=120)
    birth_date = models.DateField()
    alias = models.CharField(max_length=40)
    city = models.CharField(max_length=80, blank=True)
    gender = models.CharField(max_length=16, choices=[
        ("woman", "Woman"), ("man", "Man"), ("nonbinary", "Non-binary")])
    seeking = models.CharField(max_length=16, choices=[
        ("any", "Any"), ("woman", "Woman"), ("man", "Man"), ("nonbinary", "Non-binary")])
    intent = models.CharField(max_length=16, choices=[
        ("longterm", "Long-term"), ("explore", "Explore")], default="longterm")
    min_age = models.PositiveSmallIntegerField(default=18)
    max_age = models.PositiveSmallIntegerField(default=99)
    consent_version = models.CharField(max_length=32)
    consented_at = models.DateTimeField()
    is_visible = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
