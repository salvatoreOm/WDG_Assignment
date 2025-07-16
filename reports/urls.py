from django.urls import path
from .views import (
    ReportSubmissionView,
    BulkUploadView,
    JobStatusView,
    DashboardView,
    ReportsListView
)

urlpatterns = [
    path('report', ReportSubmissionView.as_view(), name='report-submission'),
    path('reports/upload', BulkUploadView.as_view(), name='bulk-upload'),
    path('job-status/<str:job_id>', JobStatusView.as_view(), name='job-status'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('reports', ReportsListView.as_view(), name='reports-list'),
] 