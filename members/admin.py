from django.contrib import admin

from .models import AcademyProgress, MemberProfile, SocialIdentity


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "phone", "updated_at")
    search_fields = ("display_name", "user__email", "phone")


@admin.register(SocialIdentity)
class SocialIdentityAdmin(admin.ModelAdmin):
    list_display = ("provider", "user", "email", "phone", "last_login_at")
    list_filter = ("provider",)
    search_fields = ("email", "phone", "subject", "user__email")


@admin.register(AcademyProgress)
class AcademyProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "status", "percent", "updated_at")
    list_filter = ("level", "status")
    search_fields = ("user__email", "user__username")
