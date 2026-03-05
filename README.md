# Agnes - Agricultural Farm Management Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

> A comprehensive platform designed for the agricultural community, providing essential tools and resources to enhance farming operations through efficient data exchange and management.

## 📋 Overview

Agnes is a modern farm management system that helps farmers optimize productivity by managing all nodes in the farm, from devices and sensors to locations, categories, and readings. The platform consists of multiple integrated components working together to provide a seamless agricultural management experience.

## 🏗️ Project Structure

This is a monorepo containing multiple applications and services:

```
agnes/
├── backend/
│   ├── agnes-api/          # FastAPI REST API service
│   └── agnes-workflow/     # Workflow automation service
├── frontend/
│   ├── agnes-web-app/     # Web application
│   └── agnes-cli/         # Command-line interface
└── README.md              # This file
```

### Backend Services

#### **Agnes API** (`backend/agnes-api/`)
A high-performance REST API built with FastAPI that provides:
- User management
- Device and sensor management
- Location tracking
- Category organization
- Reading data collection and storage
- Health monitoring

**Tech Stack:**
- FastAPI 0.135.1
- Pydantic 2.12.5 (with v2 validation)
- SQLAlchemy 2.0.48
- PostgreSQL (via pg8000)
- Alembic for migrations
- AWS Lambda support (via Mangum)

[📖 View API Documentation](backend/agnes-api/README.md)

#### **Agnes Workflow** (`backend/agnes-workflow/`)
Handles automated workflows and background processing for farm operations.

### Frontend Applications

#### **Agnes Web App** (`frontend/agnes-web-app/`)
Modern web interface for managing farm operations.

#### **Agnes CLI** (`frontend/agnes-cli/`)
Command-line tools for developers and system administrators.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- pip package manager

### Getting Started with the API

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agnes
   ```

2. **Set up the API service**
   ```bash
   cd backend/agnes-api
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize the database**
   ```bash
   spartan migrate init
   spartan migrate upgrade
   spartan db seed
   ```

4. **Run the development server**
   ```bash
   spartan serve
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

## 🧪 Testing

Run tests for the API service:

```bash
cd backend/agnes-api
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

## 📚 Documentation

- [API Documentation](backend/agnes-api/README.md)
- [API Reference](http://localhost:8000/docs) (when running locally)
- [Changelog](backend/agnes-api/CHANGELOG.md)
- [Contributing Guidelines](backend/agnes-api/CONTRIBUTING.md)
- [Code of Conduct](backend/agnes-api/CODE_OF_CONDUCT.md)

## 🛠️ Technology Stack

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Validation:** Pydantic v2
- **Migrations:** Alembic
- **CLI Tool:** Python Spartan
- **Cloud:** AWS Lambda ready (Mangum adapter)

### Key Features
- ✅ RESTful API architecture
- ✅ Pydantic v2 data validation
- ✅ Database migrations with Alembic
- ✅ Comprehensive test coverage
- ✅ AWS Lambda serverless deployment
- ✅ FastAPI automatic API documentation
- ✅ CORS middleware for web clients
- ✅ Environment-based configuration

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](backend/agnes-api/CONTRIBUTING.md) for details on:

- Code of conduct
- Development process
- Submitting pull requests
- Reporting bugs
- Suggesting enhancements

## 🔒 Security

If you discover any security vulnerabilities, please review our [security policy](../../security/policy) on how to report them responsibly.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Credits

- **Author:** [Sydel Palinlin](https://github.com/nerdmonkey)
- **Contributors:** [All Contributors](../../contributors)

## 🙏 Acknowledgments

Built with [Python Spartan](https://pypi.org/project/python-spartan/) - The Swiss Army knife for serverless development.

---

**Note:** Agnes is actively developed and maintained. For the latest updates, check the [Changelog](backend/agnes-api/CHANGELOG.md).
