from rest_framework import generics, status
from rest_framework.response import Response

from django.shortcuts import render
from django.utils import timezone
from django.http import FileResponse, Http404

from .models import Resume, ResumeLead, ResumeDownloadToken, Contact
from .serializers import ResumeLeadSerializer, ContactSerializer
from .tasks import send_resume_email


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ResumeLeadCreateView(generics.CreateAPIView):
    """
        Collect information of who's downloading resume and send them an email to verify if they are human and verified.
    """
    serializer_class = ResumeLeadSerializer
    queryset = ResumeLead.objects.all()

    def perform_create(self, serializer):

        request = self.request

        lead = serializer.save(
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")
        )

        # create secure token
        token_obj = ResumeDownloadToken.objects.create(
            lead=lead
        )

        # send email asynchronously
        send_resume_email.delay(
            lead.email,
            str(token_obj.token)
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")



class ResumeDownloadView(generics.GenericAPIView):
    """
     A view used to give a user access to get the copy of my resume
    """

    def get(self, request, token):

        try:
            token_obj = ResumeDownloadToken.objects.get(
                token=token,
                is_used=False
            )
        except ResumeDownloadToken.DoesNotExist:
            raise Http404("Invalid or expired link")

        if not token_obj.clicked_at:
            token_obj.clicked_at = timezone.now()
            token_obj.save(update_fields=["clicked_at"])

        return render(
            request,
            "resume/download.html",
            {"token": token_obj.token})


class ResumeFileDownloadView(generics.GenericAPIView):

    def get(self, request, token):

        try:
            token_obj = ResumeDownloadToken.objects.get(
                token=token
            )
        except ResumeDownloadToken.DoesNotExist:
            raise Http404()

        resume = Resume.objects.filter(
            is_active=True
        ).first()

        if not resume:
            raise Http404("Resume not configured")

        token_obj.downloaded_at = timezone.now()
        token_obj.is_used = True
        token_obj.save(
            update_fields=[
                "downloaded_at",
                "is_used"
            ]
        )

        response = FileResponse(
            resume.file.open("rb"),
            content_type="application/pdf"
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{resume.file.name.split("/")[-1]}"'
        )

        return response