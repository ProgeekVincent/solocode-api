from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Project,
    ProjectImage,
    ProjectHighlight,
    Technology
)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectHighlightInline(admin.TabularInline):
    model = ProjectHighlight
    extra = 1


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" width="30" height="30" />',
                obj.icon.url
            )
        return "-"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project_type",
        "repository_host",
        "repository_url",
        "demo_url",
        "featured",
        "status",
        "display_order",
        "created_at",
    )

    list_filter = (
        "status",
        "featured",
        "repository_host",
        "project_type",
        "technologies",
    )

    search_fields = (
        "title",
        "short_description",
        "description",
        "role",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    filter_horizontal = (
        "technologies",
    )

    list_editable = (
    	"featured",
        "display_order",
        "repository_host",
        "repository_url",
        "demo_url"
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "project_type",
                    "role",
                    "status",
                    "featured",
                )
            },
        ),
        (
            "Descriptions",
            {
                "fields": (
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "thumbnail",
                )
            },
        ),
        (
            "Links",
            {
                "fields": (
                    "demo_url",
                    "repository_host",
                    "repository_url"
                )
            },
        ),
        (
            "Technologies",
            {
                "fields": (
                    "technologies",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Ordering",
            {
                "fields": (
                    "display_order",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = [
        ProjectImageInline,
        ProjectHighlightInline,
    ]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "display_order",
    )

    list_filter = (
        "project",
    )


@admin.register(ProjectHighlight)
class ProjectHighlightAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "title",
    )

    search_fields = (
        "title",
    )