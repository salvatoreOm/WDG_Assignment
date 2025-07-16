from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Sum, Count
from django.db import IntegrityError
from django.http import Http404
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.openapi import OpenApiParameter
from .models import Report, Job
from .serializers import (
    ReportSerializer, BulkUploadSerializer, JobStatusSerializer, DashboardSerializer
)
from .tasks import process_csv_upload
import uuid
import logging

logger = logging.getLogger('reports')


class ReportSubmissionView(APIView):
    """
    API endpoint for submitting individual NGO reports
    POST /report
    """
    
    @extend_schema(
        summary="Submit Individual NGO Report",
        description="Submit a monthly impact report for an NGO. Supports idempotency - submitting the same NGO/month combination will update the existing report.",
        tags=["Reports"],
        request=ReportSerializer,
        responses={
            201: ReportSerializer,
            200: ReportSerializer,
            400: OpenApiExample(
                "Validation Error",
                value={"success": False, "message": "Validation failed", "errors": {}},
                response_only=True,
            ),
        },
        examples=[
            OpenApiExample(
                "Sample NGO Report",
                value={
                    "ngo_id": "NGO001",
                    "month": "2024-01",
                    "people_helped": 150,
                    "events_conducted": 5,
                    "funds_utilized": 25000.50
                },
                request_only=True,
            ),
        ],
    )
    
    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                ngo_id = serializer.validated_data['ngo_id']
                month = serializer.validated_data['month']
                
                logger.info(f"Processing report submission for NGO {ngo_id}, month {month}")
                
                # Use update_or_create for idempotency
                report, created = Report.objects.update_or_create(
                    ngo_id=ngo_id,
                    month=month,
                    defaults={
                        'people_helped': serializer.validated_data['people_helped'],
                        'events_conducted': serializer.validated_data['events_conducted'],
                        'funds_utilized': serializer.validated_data['funds_utilized'],
                    }
                )
                
                action = "created" if created else "updated"
                logger.info(f"Report {action} successfully for NGO {ngo_id}, month {month}")
                
                response_serializer = ReportSerializer(report)
                status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
                
                return Response({
                    'success': True,
                    'message': 'Report created successfully' if created else 'Report updated successfully',
                    'data': response_serializer.data
                }, status=status_code)
                
            except IntegrityError as e:
                return Response({
                    'success': False,
                    'message': 'Database error occurred',
                    'errors': [str(e)]
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class BulkUploadView(APIView):
    """
    API endpoint for bulk CSV upload
    POST /reports/upload
    """
    parser_classes = [MultiPartParser, FormParser]
    
    @extend_schema(
        summary="Bulk Upload CSV Reports",
        description="Upload a CSV file containing multiple NGO reports for background processing. Returns a job ID for tracking progress.",
        tags=["Bulk Upload"],
        request=BulkUploadSerializer,
        responses={
            202: OpenApiExample(
                "Upload Success",
                value={
                    "success": True,
                    "message": "File uploaded successfully. Processing started.",
                    "job_id": "123e4567-e89b-12d3-a456-426614174000"
                },
                response_only=True,
            ),
            400: OpenApiExample(
                "Upload Error",
                value={"success": False, "message": "File validation failed", "errors": {}},
                response_only=True,
            ),
        },
    )
    
    def post(self, request):
        serializer = BulkUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            
            try:
                logger.info(f"Starting bulk upload processing for file: {uploaded_file.name}")
                
                # Read file content
                file_content = uploaded_file.read().decode('utf-8')
                
                # Create job for tracking
                job = Job.objects.create(
                    status='pending',
                    file_name=uploaded_file.name
                )
                
                logger.info(f"Created job {job.id} for file {uploaded_file.name}")
                
                # Start background processing
                process_csv_upload.delay(str(job.id), file_content)
                
                logger.info(f"Queued background task for job {job.id}")
                
                return Response({
                    'success': True,
                    'message': 'File uploaded successfully. Processing started.',
                    'job_id': str(job.id)
                }, status=status.HTTP_202_ACCEPTED)
                
            except UnicodeDecodeError:
                return Response({
                    'success': False,
                    'message': 'Invalid file encoding. Please ensure the file is UTF-8 encoded.',
                    'errors': ['File encoding error']
                }, status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as e:
                return Response({
                    'success': False,
                    'message': 'An error occurred while processing the file',
                    'errors': [str(e)]
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': False,
            'message': 'File validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class JobStatusView(APIView):
    """
    API endpoint for checking job processing status
    GET /job-status/{job_id}
    """
    
    def get(self, request, job_id):
        try:
            # Validate UUID format
            uuid.UUID(job_id)
            job = Job.objects.get(id=job_id)
            
            serializer = JobStatusSerializer(job)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({
                'success': False,
                'message': 'Invalid job ID format'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Job.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Job not found'
            }, status=status.HTTP_404_NOT_FOUND)


class DashboardView(APIView):
    """
    API endpoint for dashboard aggregated data
    GET /dashboard?month=YYYY-MM
    """
    
    @extend_schema(
        summary="Get Dashboard Analytics",
        description="Retrieve aggregated NGO impact data for a specific month including total NGOs reporting, people helped, events conducted, and funds utilized.",
        tags=["Dashboard"],
        parameters=[
            OpenApiParameter(
                name='month',
                description='Month in YYYY-MM format (e.g., 2024-01)',
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: DashboardSerializer,
            400: OpenApiExample(
                "Invalid Month",
                value={"success": False, "message": "Invalid month format. Use YYYY-MM (e.g., 2024-01)"},
                response_only=True,
            ),
        },
        examples=[
            OpenApiExample(
                "Dashboard Response",
                value={
                    "success": True,
                    "data": {
                        "month": "2024-01",
                        "total_ngos_reporting": 25,
                        "total_people_helped": 5000,
                        "total_events_conducted": 150,
                        "total_funds_utilized": 750000.00
                    }
                },
                response_only=True,
            ),
        ],
    )
    
    def get(self, request):
        month = request.query_params.get('month')
        ngo_filter = request.query_params.get('ngo_id')
        from_month = request.query_params.get('from_month')
        to_month = request.query_params.get('to_month')
        
        # Handle single month vs date range
        if not month and not (from_month and to_month):
            return Response({
                'success': False,
                'message': 'Either month parameter (YYYY-MM) or both from_month and to_month parameters are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate month format(s)
        def validate_month_format(month_str):
            try:
                year, month_num = month_str.split('-')
                if len(year) != 4 or len(month_num) != 2:
                    raise ValueError
                if not (1 <= int(month_num) <= 12):
                    raise ValueError
                return True
            except (ValueError, IndexError):
                return False
        
        if month and not validate_month_format(month):
            return Response({
                'success': False,
                'message': 'Invalid month format. Use YYYY-MM (e.g., 2024-01)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if from_month and not validate_month_format(from_month):
            return Response({
                'success': False,
                'message': 'Invalid from_month format. Use YYYY-MM (e.g., 2024-01)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if to_month and not validate_month_format(to_month):
            return Response({
                'success': False,
                'message': 'Invalid to_month format. Use YYYY-MM (e.g., 2024-01)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Build query filters
        reports_query = Report.objects.all()
        
        if month:
            reports_query = reports_query.filter(month=month)
        elif from_month and to_month:
            reports_query = reports_query.filter(month__gte=from_month, month__lte=to_month)
        
        if ngo_filter:
            reports_query = reports_query.filter(ngo_id__icontains=ngo_filter)
        
        # Get aggregated data
        reports_for_period = reports_query
        
        aggregated_data = reports_for_period.aggregate(
            total_ngos_reporting=Count('ngo_id', distinct=True),
            total_people_helped=Sum('people_helped') or 0,
            total_events_conducted=Sum('events_conducted') or 0,
            total_funds_utilized=Sum('funds_utilized') or 0
        )
        
        # Prepare response data
        period_label = month if month else f"{from_month} to {to_month}"
        dashboard_data = {
            'period': period_label,
            'month': month,  # Keep for backward compatibility
            'filters': {
                'ngo_id': ngo_filter,
                'from_month': from_month,
                'to_month': to_month,
            },
            'total_ngos_reporting': aggregated_data['total_ngos_reporting'],
            'total_people_helped': aggregated_data['total_people_helped'],
            'total_events_conducted': aggregated_data['total_events_conducted'],
            'total_funds_utilized': aggregated_data['total_funds_utilized']
        }
        
        serializer = DashboardSerializer(dashboard_data)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ReportsListView(APIView):
    """
    API endpoint to list all reports (for debugging/admin purposes)
    GET /reports
    """
    
    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        
        return Response({
            'success': True,
            'count': len(reports),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
