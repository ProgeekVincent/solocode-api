from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


@shared_task
def send_contact_email(name, email, subject, message):
    full_subject = f"New Contact Message: {subject}"

    body = f"""
        You received a new contact message:

        Name: {name}
        Email: {email}

        Message:
        {message}
    """
    users = User.objects.filter(is_superuser=True, is_staff=True, is_active=True)
    send_mail(
        full_subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [admin.email for admin in users],
        fail_silently=False,
    )

@shared_task
def send_confirmation_email(name, email):
    subject = "Contact Confirmation"

    body = f"""
        Hi {name},

        Thanks for contacting us. We'll get back to you shortly.

    """

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [email,],
        fail_silently=False
        )



@shared_task
def send_resume_email(email, token):

    # download_link = f"{settings.FRONTEND_URL}/resume/download/{token}/"
    download_link = f"http://localhost:8000{reverse("resume-download", args=[token])}"

    subject = "Your requested resume"

    message = f"""
        Thanks for your interest.

        You can download my resume using the link below:
        {download_link}

        This link may expire for security purposes.

        If you'd like to connect, feel free to reply to this email.
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )


@shared_task
def create_resume_token(email):

    token_obj = ResumeDownloadToken.objects.create(
        email=email
    )

    return str(token_obj.token)