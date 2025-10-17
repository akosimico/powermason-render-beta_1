from django.urls import path
from .views import progress_monitoring
from . import views

urlpatterns = [
    # Session-based progress monitoring (primary)
    path("", views.progress_monitoring, name="progress_monitoring_session"),
    # Token-based progress monitoring (legacy)
    path("<str:token>/<str:role>/", views.progress_monitoring, name="progress_monitoring"),
]
