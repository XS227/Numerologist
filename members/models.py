from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="numerologist_profile")
    display_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True, db_index=True)
    picture_url = models.URLField(blank=True)
    complimentary_access = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.display_name or self.user.email or self.user.username


class SocialIdentity(models.Model):
    PROVIDERS = (("vipps", "Vipps"), ("google", "Google"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_identities")
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    subject = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("provider", "subject"), name="unique_social_subject")]

    def __str__(self) -> str:
        return f"{self.provider}:{self.subject}"


class SocialLoginHandoff(models.Model):
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    provider = models.CharField(max_length=20)
    payload = models.JSONField(default=dict)
    next_url = models.CharField(max_length=500, default="/min-side/")
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.provider}:{self.created_at.isoformat()}"


class AcademyProgress(models.Model):
    STATUS = (("locked", "Locked"), ("active", "Active"), ("completed", "Completed"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="academy_progress")
    level = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=16, choices=STATUS, default="locked")
    percent = models.PositiveSmallIntegerField(default=0)
    homework = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "level"), name="unique_academy_level_progress")]
        ordering = ("level",)

    def __str__(self) -> str:
        return f"{self.user_id}: level {self.level} ({self.status})"
