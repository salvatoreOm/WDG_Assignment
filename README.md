# NGO Impact Tracker

A scalable web application that enables NGOs across India to submit monthly impact reports and provides administrators with a comprehensive dashboard to track and analyze aggregated data.

## 🚀 Deployed Application

**Live Demo**: [https://wdg-assignment-smcb.vercel.app](https://wdg-assignment-smcb.vercel.app)

## 🛠 Tech Stack

### Backend
- **Django 5.2.4** - Web framework
- **Django REST Framework** - API development
- **Celery** - Background task processing
- **Redis** - Message broker for Celery
- **SQLite** - Database

### Frontend
- **React 19** - Frontend framework
- **Material-UI (MUI)** - Component library and styling
- **Axios** - HTTP client for API communication

### Deployment
- **Vercel** - Frontend hosting
- **Railway/Heroku** - Backend deployment options

## 📋 Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 14+
- Redis server

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/salvatoreOm/WDG_Assignment.git
   cd WDG_Assignment
   ```

2. **Backend Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. **Start Services** (3 separate terminals):
   ```bash
   # Terminal 1: Redis
   redis-server
   
   # Terminal 2: Celery Worker
   celery -A ngo_impact_tracker worker --loglevel=info
   
   # Terminal 3: Django Server
   python manage.py runserver
   ```

4. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

**Application URLs**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- API Documentation: http://localhost:8000/api/docs/

## 📡 API Sample Usage

### Submit Single Report
```bash
curl -X POST http://localhost:8000/api/report \
  -H "Content-Type: application/json" \
  -d '{
    "ngo_id": "NGO001",
    "month": "2024-01",
    "people_helped": 150,
    "events_conducted": 5,
    "funds_utilized": 25000.50
  }'
```

### Bulk Upload CSV
```bash
curl -X POST http://localhost:8000/api/reports/upload \
  -F "file=@sample_reports.csv"
```

### Check Processing Status
```bash
curl http://localhost:8000/api/job-status/{job_id}
```

### Dashboard Data
```bash
curl "http://localhost:8000/api/dashboard?month=2024-01"
```

## 🖥 UI Features

The application includes:
- **Individual Report Submission**: Clean form with validation
- **Bulk CSV Upload**: Drag-and-drop interface with real-time progress tracking
- **Admin Dashboard**: Aggregated metrics with filtering capabilities
- **Status Tracking**: Live updates for background processing jobs
- **Responsive Design**: Mobile-friendly Material-UI components

## 📝 Technical Writeup

### Approach & Architecture

I designed this application with scalability and user experience as primary considerations. The architecture follows a clean separation between frontend and backend, enabling independent scaling and deployment.

**Backend Architecture**: I chose Django REST Framework for rapid API development with built-in validation and serialization. Celery with Redis handles asynchronous CSV processing, preventing timeout issues during bulk uploads. The database design enforces idempotency through unique constraints on (ngo_id, month) pairs, preventing duplicate submissions.

**Frontend Architecture**: React with Material-UI provides a professional, responsive interface. I implemented real-time progress tracking using polling to give users feedback during long-running operations. The component structure is modular and reusable.

**Key Design Decisions**:
- Asynchronous processing for scalability
- Comprehensive error handling and validation
- Progress tracking for better UX
- RESTful API design for clarity

### AI Tools Usage

I leveraged AI assistance primarily for:
- Boilerplate code generation and Django model setup
- API endpoint documentation and validation logic
- Frontend component structure and Material-UI integration
- Error handling patterns and best practices
- Deployment configuration troubleshooting

### Production Improvements

With more time, I would implement:
- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Database Migration**: PostgreSQL with connection pooling and proper indexing
- **Caching Strategy**: Redis caching for dashboard aggregations
- **Monitoring**: Structured logging, health checks, and performance monitoring
- **Testing**: Comprehensive unit, integration, and end-to-end testing
- **Security**: Rate limiting, input sanitization, and HTTPS configuration
- **CI/CD Pipeline**: Automated testing and deployment workflows
