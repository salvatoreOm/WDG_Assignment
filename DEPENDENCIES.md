# Dependencies - NGO Impact Tracker

## Python Dependencies (Backend)

### Core Framework
- **Django 5.2.4** - Web framework
- **djangorestframework 3.16.0** - REST API framework
- **django-cors-headers 4.7.0** - CORS handling for React integration

### Database & Storage
- **sqlparse 0.5.3** - SQL parsing utilities (Django dependency)
- **asgiref 3.9.1** - ASGI utilities (Django dependency)

### Background Processing
- **celery 5.5.3** - Distributed task queue
- **redis 6.2.0** - Message broker for Celery
- **kombu 5.5.4** - Messaging library (Celery dependency)
- **billiard 4.2.1** - Process pool library (Celery dependency)
- **vine 5.1.0** - Python promises (Celery dependency)
- **amqp 5.3.1** - AMQP library (Celery dependency)

### CLI & Utilities
- **click 8.2.1** - Command line interface creation
- **click-didyoumean 0.3.1** - Click plugin for suggestions
- **click-plugins 1.1.1.2** - Click plugin support
- **click-repl 0.3.0** - Click REPL support
- **prompt_toolkit 3.0.51** - Command line interface building

### HTTP & Network
- **requests 2.32.4** - HTTP library for testing
- **urllib3 2.5.0** - HTTP client (requests dependency)
- **certifi 2025.7.14** - Certificate bundle (requests dependency)
- **charset-normalizer 3.4.2** - Character encoding detection
- **idna 3.10** - Internationalized domain names

### Date & Time
- **python-dateutil 2.9.0.post0** - Date utilities
- **tzdata 2025.2** - Timezone data

### Utilities
- **packaging 25.0** - Package utilities
- **six 1.17.0** - Python 2/3 compatibility
- **wcwidth 0.2.13** - Terminal width calculations

## Frontend Dependencies (React)

### Core Framework
- **React 18.x** - Frontend framework
- **React DOM 18.x** - DOM rendering for React
- **React Scripts** - Build tools and development server

### UI Components
- **@mui/material** - Material-UI components
- **@emotion/react** - CSS-in-JS styling
- **@emotion/styled** - Styled components
- **@mui/icons-material** - Material-UI icons

### HTTP Client
- **axios** - Promise-based HTTP client

### Development Tools
- **ESLint** - Code linting
- **Prettier** (if configured) - Code formatting
- **Web Vitals** - Performance metrics

## System Dependencies

### Required Services
- **Redis Server** - Message broker for Celery
- **Node.js 14+** - JavaScript runtime for React
- **Python 3.8+** - Python runtime

### Development Tools
- **npm/yarn** - Node.js package manager
- **pip** - Python package manager

## Installation Commands

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install Python dependencies
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

### System Services
```bash
# Install Redis
brew install redis  # macOS
sudo apt-get install redis-server  # Ubuntu
```

## Development vs Production

### Development
- SQLite database (included)
- Django development server
- React development server
- Local Redis instance

### Production Recommendations
- PostgreSQL database
- Gunicorn/uWSGI application server
- Nginx reverse proxy
- Redis Cluster
- Docker containers
- Cloud storage for media files

## Security Considerations

### Current (Development)
- Basic Django security settings
- CORS configuration for localhost
- SQLite file-based database

### Production Requirements
- Environment-based secrets management
- HTTPS/SSL configuration
- Database connection security
- Redis authentication
- Rate limiting
- Input sanitization
- JWT authentication

## Version Compatibility

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Node.js**: 14.x, 16.x, 18.x, 20.x
- **Redis**: 6.x, 7.x
- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Updates & Maintenance

### Regular Updates
```bash
# Backend
pip list --outdated
pip install --upgrade <package-name>

# Frontend
npm outdated
npm update
```

### Security Updates
```bash
# Backend
pip-audit  # (install: pip install pip-audit)

# Frontend
npm audit
npm audit fix
``` 