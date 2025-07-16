# NGO Impact Tracker

A scalable web application that enables NGOs across India to submit monthly impact reports and provides administrators with a comprehensive dashboard to track and analyze aggregated data.

## Tech Stack

### Backend
- **Django 5.2.4** - Web framework
- **Django REST Framework** - API development
- **Celery** - Background task processing
- **Redis** - Message broker for Celery
- **SQLite** - Database (easily configurable for PostgreSQL/MySQL)

### Frontend
- **React 18** - Frontend framework
- **Material-UI (MUI)** - Component library and styling
- **Axios** - HTTP client for API communication

## Features

### Core Functionality
- ✅ Individual monthly report submission
- ✅ Bulk CSV upload with background processing
- ✅ Real-time job progress tracking
- ✅ Admin dashboard with aggregated metrics
- ✅ Data validation and error handling
- ✅ Idempotency (prevents duplicate reports for same NGO/month)

### Technical Features
- ✅ Asynchronous CSV processing
- ✅ Partial failure handling
- ✅ Progress tracking with polling
- ✅ Responsive design
- ✅ CORS configuration for frontend-backend communication
- ✅ Comprehensive error handling and validation

## API Endpoints

### 1. Submit Single Report
```
POST /api/report
Content-Type: application/json

{
  "ngo_id": "NGO001",
  "month": "2024-01",
  "people_helped": 150,
  "events_conducted": 5,
  "funds_utilized": 25000.50
}
```

### 2. Bulk Upload CSV
```
POST /api/reports/upload
Content-Type: multipart/form-data

Form data:
- file: CSV file with columns (ngo_id, month, people_helped, events_conducted, funds_utilized)

Response:
{
  "success": true,
  "message": "File uploaded successfully. Processing started.",
  "job_id": "uuid"
}
```

### 3. Job Status Tracking
```
GET /api/job-status/{job_id}

Response:
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "processing",
    "total_rows": 100,
    "processed_rows": 45,
    "successful_rows": 42,
    "failed_rows": 3,
    "progress_percentage": 45.0,
    "error_details": [...]
  }
}
```

### 4. Dashboard Data
```
GET /api/dashboard?month=2024-01

Response:
{
  "success": true,
  "data": {
    "month": "2024-01",
    "total_ngos_reporting": 25,
    "total_people_helped": 5000,
    "total_events_conducted": 150,
    "total_funds_utilized": 750000.00
  }
}
```

## Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 14+
- Redis server

### Backend Setup

1. **Clone and navigate to the project**:
   ```bash
   git clone <repository-url>
   cd WDG_Assignment
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install django djangorestframework celery redis django-cors-headers
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start Redis server** (in a separate terminal):
   ```bash
   redis-server
   ```

6. **Start Celery worker** (in a separate terminal):
   ```bash
   source venv/bin/activate
   celery -A ngo_impact_tracker worker --loglevel=info
   ```

7. **Start Django development server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start React development server**:
   ```bash
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api

## Sample CSV Format

Download the sample CSV from the application or create a file with these columns:

```csv
ngo_id,month,people_helped,events_conducted,funds_utilized
NGO001,2024-01,150,5,25000.50
NGO002,2024-01,200,8,35000.00
NGO001,2024-02,175,6,28000.75
```

## Usage Examples

### Submit Individual Report
1. Navigate to "Submit Report" tab
2. Fill in NGO ID, month (YYYY-MM format), and impact metrics
3. Click "Submit Report"
4. View success/error feedback

### Bulk Upload
1. Navigate to "Bulk Upload" tab
2. Download sample CSV for reference
3. Upload your CSV file
4. Monitor real-time progress
5. Review processing results and errors

### View Dashboard
1. Navigate to "Dashboard" tab
2. Select desired month
3. View aggregated metrics and insights
4. Analyze NGO impact data

## Architecture Decisions

### Database Design
- **Reports Table**: Stores individual NGO reports with unique constraint on (ngo_id, month) for idempotency
- **Jobs Table**: Tracks background processing status with detailed progress information

### Background Processing
- **Celery Integration**: Handles CSV processing asynchronously to prevent timeouts
- **Progress Tracking**: Real-time updates during processing with error collection
- **Partial Failure Handling**: Continues processing valid rows even when some fail

### Frontend Architecture
- **Component-Based Design**: Modular React components for maintainability
- **Material-UI Integration**: Professional, responsive design
- **API Service Layer**: Centralized API communication with error handling

### Scalability Considerations
- **Database Indexing**: Optimized queries with proper indexing on frequently accessed fields
- **Async Processing**: Non-blocking CSV uploads with background processing
- **Error Isolation**: Individual row failures don't stop entire batch processing

## Production Improvements

Given more time, the following enhancements would be implemented:

### Infrastructure
- **Database Migration**: PostgreSQL with connection pooling
- **Caching Layer**: Redis for frequently accessed dashboard data
- **File Storage**: AWS S3 for CSV file storage
- **Container Deployment**: Docker containers with orchestration

### Security
- **Authentication & Authorization**: JWT-based auth with role-based access
- **Rate Limiting**: API throttling to prevent abuse
- **Input Sanitization**: Enhanced validation and sanitization
- **HTTPS Configuration**: SSL/TLS encryption

### Monitoring & Performance
- **Logging System**: Structured logging with ELK stack
- **Performance Monitoring**: Application performance monitoring
- **Health Checks**: System health monitoring and alerting
- **Database Optimization**: Query optimization and indexing

### Features
- **Data Export**: Export dashboard data to Excel/PDF
- **Advanced Filtering**: Date ranges, NGO filtering, regional analysis
- **Notifications**: Email/SMS notifications for report submissions
- **Audit Trail**: Track all data changes for compliance

### Testing
- **Unit Tests**: Comprehensive backend and frontend test coverage
- **Integration Tests**: API endpoint testing
- **Load Testing**: Performance testing for scalability
- **E2E Testing**: Complete workflow testing

## Screenshots

The application includes:
- Clean, professional interface with Material-UI components
- Real-time progress tracking for bulk uploads
- Interactive dashboard with metric cards and insights
- Comprehensive error handling and user feedback
- Mobile-responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is developed for educational and demonstration purposes.
