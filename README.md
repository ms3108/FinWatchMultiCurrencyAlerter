# Fin-Watch: Multi-Currency FX Alerter

A backend microservice that provides real-time currency exchange data, executes conversions, and offers a user-defined alerting system.

## 🚀 Features

- **Real-time Currency Exchange Data**: Get live exchange rates for multiple currencies
- **Currency Conversion**: Execute real-time currency conversions
- **User-Defined Alerts**: Set custom alerts for currency rate changes
- **User Management**: User registration and authentication system
- **RESTful API**: FastAPI-based REST API with automatic documentation
- **Database Integration**: PostgreSQL database with SQLAlchemy ORM
- **Dockerized Deployment**: Easy deployment with Docker and Docker Compose

## 🏗️ Architecture

The application follows a modular architecture with the following components:

```
app/
├── api/           # API endpoints and routes
├── core/          # Core configuration and security
├── crud/          # Database CRUD operations
├── db/            # Database models and session management
├── schemas/       # Pydantic schemas for data validation
├── services/      # Business logic and external services
└── main.py        # FastAPI application entry point

background/        # Background services and tasks
frontend/          # Frontend application (if applicable)
tests/            # Test files
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt
- **Task Scheduling**: APScheduler
- **Containerization**: Docker & Docker Compose
- **API Documentation**: Automatic with FastAPI (Swagger/OpenAPI)

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- PostgreSQL (if running without Docker)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ms3108/Real-Time-Ride-Sharing-Analytics-Platform.git
   cd Real-Time-Ride-Sharing-Analytics-Platform
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Redoc Documentation: http://localhost:8000/redoc

### Local Development

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database** and update `.env` file

4. **Initialize the database**:
   ```bash
   python init_db.py
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🔧 Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=finwatch_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (for external services)
# Add your API keys here
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Main Endpoints

- `GET /` - Welcome message and health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /currencies/rates` - Get current exchange rates
- `POST /currencies/convert` - Convert between currencies
- `POST /alerts/create` - Create currency alert
- `GET /alerts/` - Get user alerts

## 🧪 Testing

Run the test suite:

```bash
# Using pytest
pytest tests/

# With coverage
pytest --cov=app tests/
```

## 🐳 Docker Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild specific service
docker-compose build app
```

## 📁 Project Structure

```
Real-Time-Ride-Sharing-Analytics-Platform/
├── app/
│   ├── api/              # API route handlers
│   ├── core/             # Core functionality (security, config)
│   ├── crud/             # Database CRUD operations
│   ├── db/               # Database models and session
│   ├── schemas/          # Pydantic models
│   ├── services/         # Business logic
│   └── main.py           # FastAPI app creation and configuration
├── background/           # Background services
├── frontend/            # Frontend application
├── tests/               # Test files
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile          # Docker image configuration
├── requirements.txt    # Python dependencies
├── init_db.py         # Database initialization script
├── wait_for_db.py     # Database readiness check
└── .env               # Environment variables
```
