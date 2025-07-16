from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Sum, Count
from django.db import IntegrityError
from django.http import Http404
from .models import Report, Job
from .serializers import (
    ReportSerializer, BulkUploadSerializer, JobStatusSerializer, DashboardSerializer
)
from .tasks import process_csv_upload
import uuid


class ReportSubmissionView(APIView):
    """
    API endpoint for submitting individual NGO reports
    POST /report
    """
    
    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Use update_or_create for idempotency
                report, created = Report.objects.update_or_create(
                    ngo_id=serializer.validated_data['ngo_id'],
                    month=serializer.validated_data['month'],
                    defaults={
                        'people_helped': serializer.validated_data['people_helped'],
                        'events_conducted': serializer.validated_data['events_conducted'],
                        'funds_utilized': serializer.validated_data['funds_utilized'],
                    }
                )
                
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
    
    def post(self, request):
        serializer = BulkUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            
            try:
                # Read file content
                file_content = uploaded_file.read().decode('utf-8')
                
                # Create job for tracking
                job = Job.objects.create(
                    status='pending',
                    file_name=uploaded_file.name
                )
                
                # Start background processing
                process_csv_upload.delay(str(job.id), file_content)
                
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
    
    def get(self, request):
        month = request.query_params.get('month')
        
        if not month:
            return Response({
                'success': False,
                'message': 'Month parameter is required (format: YYYY-MM)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate month format
        try:
            year, month_num = month.split('-')
            if len(year) != 4 or len(month_num) != 2:
                raise ValueError
            if not (1 <= int(month_num) <= 12):
                raise ValueError
        except (ValueError, IndexError):
            return Response({
                'success': False,
                'message': 'Invalid month format. Use YYYY-MM (e.g., 2024-01)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get aggregated data for the specified month
        reports_for_month = Report.objects.filter(month=month)
        
        aggregated_data = reports_for_month.aggregate(
            total_ngos_reporting=Count('ngo_id', distinct=True),
            total_people_helped=Sum('people_helped') or 0,
            total_events_conducted=Sum('events_conducted') or 0,
            total_funds_utilized=Sum('funds_utilized') or 0
        )
        
        # Prepare response data
        dashboard_data = {
            'month': month,
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
