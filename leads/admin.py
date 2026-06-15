from django.contrib import admin

from .models import Resume, ResumeLead, ResumeDownloadToken

@admin.register(Resume)
class RegisterAdmin(admin.ModelAdmin):
	list_display = ["title", "file", "is_active"]


@admin.register(ResumeLead)
class ResumeLeadAdmin(admin.ModelAdmin):
	list_display = ["email", "full_name", "role", "company", "reason", "ip_address", "user_agent"]
	list_filter = ["role", "reason"]

@admin.register(ResumeDownloadToken)
class ResumeDownloadToken(admin.ModelAdmin):
	list_display = ["lead", "token", "clicked_at", "downloaded_at", "is_used", "created_at"]