from django.urls import path
from .views import ContactCreateView, ResumeLeadCreateView, ResumeDownloadView, ResumeFileDownloadView

urlpatterns = [
    path("contact/", ContactCreateView.as_view()),
    path("resume/request/", ResumeLeadCreateView.as_view()),
    path("resume/download/<uuid:token>/", ResumeDownloadView.as_view(), 
        name="resume-download"),
    path("resume/file/download/<uuid:token>/", ResumeFileDownloadView.as_view(), name="resume-file-download")
]