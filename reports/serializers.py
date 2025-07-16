from rest_framework import serializers
from .models import Report, Job


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for individual NGO reports"""
    
    class Meta:
        model = Report
        fields = ['ngo_id', 'month', 'people_helped', 'events_conducted', 'funds_utilized', 'created_at']
        read_only_fields = ['created_at']

    def validate_month(self, value):
        """Validate month format"""
        try:
            year, month = value.split('-')
            if len(year) != 4 or len(month) != 2:
                raise ValueError
            if not (1 <= int(month) <= 12):
                raise ValueError
        except (ValueError, IndexError):
            raise serializers.ValidationError("Month must be in YYYY-MM format (e.g., 2024-01)")
        return value

    def validate_ngo_id(self, value):
        """Validate NGO ID is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("NGO ID cannot be empty")
        return value.strip()


class BulkUploadSerializer(serializers.Serializer):
    """Serializer for CSV file uploads"""
    file = serializers.FileField()

    def validate_file(self, value):
        """Validate the uploaded file"""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed")
        
        # Check file size (limit to 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        return value


class JobStatusSerializer(serializers.ModelSerializer):
    """Serializer for job status tracking"""
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'status', 'total_rows', 'processed_rows', 'successful_rows', 
            'failed_rows', 'progress_percentage', 'error_details', 'file_name',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardSerializer(serializers.Serializer):
    """Serializer for dashboard aggregated data"""
    month = serializers.CharField()
    total_ngos_reporting = serializers.IntegerField()
    total_people_helped = serializers.IntegerField()
    total_events_conducted = serializers.IntegerField()
    total_funds_utilized = serializers.DecimalField(max_digits=15, decimal_places=2) 