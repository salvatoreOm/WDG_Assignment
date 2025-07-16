from django.contrib import admin
from .models import Report, Job

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['ngo_id', 'month', 'people_helped', 'events_conducted', 'funds_utilized', 'created_at']
    list_filter = ['month', 'created_at']
    search_fields = ['ngo_id', 'month']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'file_name', 'total_rows', 'processed_rows', 'successful_rows', 'failed_rows', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['file_name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'progress_percentage']
    
    def progress_percentage(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage.short_description = "Progress"
