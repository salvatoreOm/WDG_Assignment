# NGO Impact Tracker - API Documentation

## 🚀 Interactive API Documentation

The NGO Impact Tracker now includes **comprehensive OpenAPI/Swagger documentation** with interactive testing capabilities.

### Access Documentation

| Documentation Type | URL | Description |
|-------------------|-----|-------------|
| **Swagger UI** | http://localhost:8000/api/docs/ | Interactive API testing interface |
| **ReDoc** | http://localhost:8000/api/redoc/ | Clean, readable documentation |
| **OpenAPI Schema** | http://localhost:8000/api/schema/ | Raw OpenAPI 3.0 specification |

## 📊 Enhanced Features

### 1. Dashboard Filtering & Analytics
- **Date Range Support**: Query data across multiple months
- **NGO Filtering**: Filter by specific NGO ID
- **Combined Filters**: Mix and match filters for detailed analysis

#### New Query Parameters:
```bash
# Single month (original)
GET /api/dashboard?month=2024-01

# Date range filtering
GET /api/dashboard?from_month=2024-01&to_month=2024-03

# NGO-specific filtering
GET /api/dashboard?month=2024-01&ngo_id=NGO001

# Combined filtering
GET /api/dashboard?from_month=2024-01&to_month=2024-03&ngo_id=NGO001
```

#### Enhanced Response Format:
```json
{
  "success": true,
  "data": {
    "period": "2024-01 to 2024-03",
    "month": null,
    "filters": {
      "ngo_id": "NGO001",
      "from_month": "2024-01",
      "to_month": "2024-03"
    },
    "total_ngos_reporting": 15,
    "total_people_helped": 2500,
    "total_events_conducted": 75,
    "total_funds_utilized": 375000.00
  }
}
```

### 2. Structured Logging & Observability
- **JSON-formatted logs** for easy parsing
- **Separate log files** for Django and Celery
- **Request tracking** with correlation IDs
- **Performance metrics** logging

#### Log Files:
- `django.log` - Django application logs
- `celery.log` - Background task processing logs

#### Sample Log Entry:
```json
{
  "level": "INFO",
  "time": "2024-01-15 10:30:45,123",
  "module": "views",
  "message": "Report created successfully for NGO NGO001, month 2024-01"
}
```

### 3. Enhanced UI Components
- **Status Chips**: Consistent status indicators across the application
- **Progress Indicators**: Real-time visual feedback
- **Filter Chips**: Visual representation of active filters
- **Responsive Grid Layout**: Optimized for all screen sizes

## 🛠️ API Endpoints Reference

### Reports Management

#### Submit Individual Report
```http
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

**Features:**
- ✅ Automatic validation
- ✅ Idempotency support
- ✅ Detailed error messages
- ✅ Structured logging

#### Bulk CSV Upload
```http
POST /api/reports/upload
Content-Type: multipart/form-data

Form Data:
- file: [CSV file]
```

**CSV Format:**
```csv
ngo_id,month,people_helped,events_conducted,funds_utilized
NGO001,2024-01,150,5,25000.50
NGO002,2024-01,200,8,35000.00
```

**Features:**
- ✅ Background processing
- ✅ Real-time progress tracking
- ✅ Partial failure handling
- ✅ Detailed error reporting

#### Job Status Monitoring
```http
GET /api/job-status/{job_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "processing",
    "total_rows": 100,
    "processed_rows": 45,
    "successful_rows": 42,
    "failed_rows": 3,
    "progress_percentage": 45.0,
    "error_details": [
      {
        "row": 15,
        "error": "Invalid month format",
        "data": {"ngo_id": "NGO015", "month": "2024-13"}
      }
    ]
  }
}
```

### Analytics Dashboard

#### Get Aggregated Data
```http
# Single month
GET /api/dashboard?month=2024-01

# Date range
GET /api/dashboard?from_month=2024-01&to_month=2024-03

# With NGO filter
GET /api/dashboard?month=2024-01&ngo_id=NGO001
```

**Features:**
- ✅ Flexible date filtering
- ✅ NGO-specific analytics
- ✅ Aggregated metrics
- ✅ Performance insights

## 🧪 Testing the API

### Using Swagger UI (Recommended)
1. Navigate to http://localhost:8000/api/docs/
2. Expand any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Execute the request
6. View the response

### Using curl
```bash
# Submit a report
curl -X POST "http://localhost:8000/api/report" \
  -H "Content-Type: application/json" \
  -d '{
    "ngo_id": "NGO001",
    "month": "2024-01",
    "people_helped": 150,
    "events_conducted": 5,
    "funds_utilized": 25000.50
  }'

# Get dashboard data
curl "http://localhost:8000/api/dashboard?month=2024-01"

# Upload CSV file
curl -X POST "http://localhost:8000/api/reports/upload" \
  -F "file=@sample_reports.csv"
```

### Using the Test Script
```bash
python test_api.py
```

## 📈 Performance & Monitoring

### Logging Levels
- **DEBUG**: Development debugging
- **INFO**: General application flow
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **CRITICAL**: Critical failures

### Monitoring Metrics
- API response times
- Background job processing times
- Database query performance
- Error rates and types
- User activity patterns

### Health Check Endpoints
```http
GET /api/reports  # Basic connectivity test
GET /admin/       # Admin interface availability
```

## 🔧 Development Tools

### Swagger Features
- **Interactive Testing**: Execute API calls directly from documentation
- **Schema Validation**: Automatic request/response validation
- **Code Generation**: Generate client SDKs in multiple languages
- **Export Options**: Download OpenAPI spec for external tools

### Logging Integration
- **Centralized Logging**: All components log to structured format
- **Correlation IDs**: Track requests across services
- **Performance Metrics**: Built-in timing and performance data
- **Error Context**: Detailed error information with stack traces

## 🚀 Production Considerations

### Security
- Add authentication to Swagger endpoints
- Implement rate limiting
- Enable HTTPS only
- Sanitize log data

### Performance
- Implement response caching
- Database query optimization
- Background job queue scaling
- CDN for static assets

### Monitoring
- APM integration (e.g., New Relic, DataDog)
- Log aggregation (e.g., ELK Stack)
- Alerting on error thresholds
- Performance dashboards

## 📚 Additional Resources

- **OpenAPI Specification**: https://swagger.io/specification/
- **DRF Spectacular Documentation**: https://drf-spectacular.readthedocs.io/
- **Material-UI Components**: https://mui.com/components/
- **Django Logging**: https://docs.djangoproject.com/en/stable/topics/logging/ 