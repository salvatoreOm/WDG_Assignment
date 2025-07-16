import csv
import io
from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.utils import timezone
from .models import Report, Job
from decimal import Decimal, InvalidOperation


@shared_task(bind=True)
def process_csv_upload(self, job_id, file_content):
    """
    Background task to process CSV file uploads.
    Handles validation, creation of reports, and progress tracking.
    """
    try:
        job = Job.objects.get(id=job_id)
        job.status = 'processing'
        job.save()

        # Parse CSV content
        csv_reader = csv.DictReader(io.StringIO(file_content))
        
        # Expected columns
        required_columns = ['ngo_id', 'month', 'people_helped', 'events_conducted', 'funds_utilized']
        
        # Validate headers
        headers = csv_reader.fieldnames
        if not headers:
            job.status = 'failed'
            job.error_details = [{'error': 'Empty CSV file or no headers found'}]
            job.save()
            return

        missing_columns = [col for col in required_columns if col not in headers]
        if missing_columns:
            job.status = 'failed'
            job.error_details = [{'error': f'Missing required columns: {", ".join(missing_columns)}'}]
            job.save()
            return

        # Count total rows for progress tracking
        rows = list(csv_reader)
        job.total_rows = len(rows)
        job.save()

        if job.total_rows == 0:
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            return

        errors = []
        successful_count = 0
        failed_count = 0

        for row_num, row in enumerate(rows, start=1):
            try:
                # Clean and validate data
                ngo_id = row.get('ngo_id', '').strip()
                month = row.get('month', '').strip()
                
                if not ngo_id:
                    raise ValueError("NGO ID cannot be empty")
                
                if not month:
                    raise ValueError("Month cannot be empty")

                # Validate and convert numeric fields
                try:
                    people_helped = int(row.get('people_helped', 0))
                    if people_helped < 0:
                        raise ValueError("People helped cannot be negative")
                except (ValueError, TypeError):
                    raise ValueError("People helped must be a valid non-negative number")

                try:
                    events_conducted = int(row.get('events_conducted', 0))
                    if events_conducted < 0:
                        raise ValueError("Events conducted cannot be negative")
                except (ValueError, TypeError):
                    raise ValueError("Events conducted must be a valid non-negative number")

                try:
                    funds_utilized = Decimal(str(row.get('funds_utilized', 0)))
                    if funds_utilized < 0:
                        raise ValueError("Funds utilized cannot be negative")
                except (InvalidOperation, ValueError, TypeError):
                    raise ValueError("Funds utilized must be a valid non-negative number")

                # Create or update report (handles idempotency)
                with transaction.atomic():
                    report, created = Report.objects.update_or_create(
                        ngo_id=ngo_id,
                        month=month,
                        defaults={
                            'people_helped': people_helped,
                            'events_conducted': events_conducted,
                            'funds_utilized': funds_utilized,
                        }
                    )
                    successful_count += 1

            except (ValueError, ValidationError, IntegrityError) as e:
                failed_count += 1
                errors.append({
                    'row': row_num,
                    'data': row,
                    'error': str(e)
                })

            # Update progress
            job.processed_rows = row_num
            job.successful_rows = successful_count
            job.failed_rows = failed_count
            job.error_details = errors
            job.save()

        # Mark job as completed
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.save()

    except Job.DoesNotExist:
        # Job was deleted or doesn't exist
        return
    except Exception as e:
        # Handle unexpected errors
        try:
            job = Job.objects.get(id=job_id)
            job.status = 'failed'
            job.error_details = [{'error': f'Unexpected error: {str(e)}'}]
            job.save()
        except Job.DoesNotExist:
            pass 