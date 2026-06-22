import os
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify



def validate_svg(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext != ".svg":
        raise ValidationError("Only SVG files are allowed.")

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.FileField(
    	upload_to="technologies/icons/", 
    	blank=True, 
    	null=True,
    	validators=[validate_svg]
    	)

    def __str__(self):
        return self.name

    class Meta:
    	verbose_name_plural = "Technologies"


class Project(models.Model):

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    PROJECT_TYPES = [
	    ("personal", "Personal"),
	    ("client", "Client"),
	    ("startup", "Startup"),
	    ("academic", "Academic"),
	    ("open_source", "Open Source"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.CharField(max_length=300)

    description = models.TextField( help_text="Detailed project description" )

    thumbnail = models.ImageField( upload_to="projects/thumbnails/" )

    technologies = models.ManyToManyField(
        Technology,
        related_name="projects",
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="completed"
    )

    project_type = models.CharField(
    	max_length=50,
    	choices=PROJECT_TYPES,
    	default="personal"
    	)

    role = models.CharField(
    	max_length=255,
    	help_text="Your role in the project"
    	)

    featured = models.BooleanField(default=False)
    demo_url = models.URLField(blank=True)
    repository_host = models.CharField(max_length=300, blank=True)
    repository_url = models.URLField(blank=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="projects/gallery/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.project.title} Image"





class ProjectHighlight(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="highlights"
    )

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title