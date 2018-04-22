from django.urls import path

from django.conf import settings
from CS415.views import SubmissionOneView, SubmissionTwoView

urlpatterns = [
    path('submissions/1/', SubmissionOneView.as_view()),
    path(settings.SUBMISSION_2_PATH, SubmissionTwoView.as_view()),
]
