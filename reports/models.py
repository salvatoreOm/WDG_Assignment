from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import uuid

class Report(models.Model):
    """
    Model to store monthly NGO reports.
    Ensures idempotency with unique constraint on ngo_id + month.
    """
    ngo_id = models.CharField(max_length=100, help_text="NGO identifier")
    month = models.CharField(max_length=7, help_text="Report month in YYYY-MM format")
    people_helped = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of people helped this month"
    )
    events_conducted = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of events conducted this month"
    )
    funds_utilized = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Amount of funds utilized this month"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure one report per NGO per month (idempotency)
        unique_together = ['ngo_id', 'month']
        ordering = ['-created_at']

    def clean(self):
        """Validate month format"""
        super().clean()
        if self.month:
            try:
                year, month = self.month.split('-')
                if len(year) != 4 or len(month) != 2:
                    raise ValueError
                if not (1 <= int(month) <= 12):
                    raise ValueError
            except (ValueError, IndexError):
                raise ValidationError({
                    'month': 'Month must be in YYYY-MM format (e.g., 2024-01)'
                })

    def __str__(self):
        return f"{self.ngo_id} - {self.month}"


class Job(models.Model):
    """
    Model to track background job processing status for CSV uploads.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_rows = models.PositiveIntegerField(default=0, help_text="Total rows to process")
    processed_rows = models.PositiveIntegerField(default=0, help_text="Rows processed so far")
    successful_rows = models.PositiveIntegerField(default=0, help_text="Successfully processed rows")
    failed_rows = models.PositiveIntegerField(default=0, help_text="Failed rows")
    error_details = models.JSONField(default=list, blank=True, help_text="List of errors encountered")
    file_name = models.CharField(max_length=255, blank=True, help_text="Original filename")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def progress_percentage(self):
        """Calculate processing progress as percentage"""
        if self.total_rows == 0:
            return 0
        return round((self.processed_rows / self.total_rows) * 100, 2)

    def __str__(self):
        return f"Job {self.id} - {self.status}"
