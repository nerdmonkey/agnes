![Agnes Platform](docs/agnes.svg)

# Agnes - Agricultural Farm Management Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

> A comprehensive platform designed for the agricultural community, providing essential tools and resources to enhance farming operations through efficient data exchange and management.

## 📋 Overview

Agnes is a modern farm management system that helps farmers optimize productivity by managing all nodes in the farm, from devices and sensors to locations, categories, and readings. The platform consists of multiple integrated components including a REST API backend, web application frontend, CLI tools, and workflow orchestration with n8n, working together to provide a seamless agricultural management experience.

## 🏗️ Project Structure

This is a monorepo containing multiple applications and services:

```
agnes/
├── backend/               # Agnes API - FastAPI REST API service
├── frontend/              # Agnes Web App - Next.js application
├── setup/                 # Installation and setup scripts
├── .gitignore
├── LICENSE
└── README.md
```

### 🔌 Backend Services

#### **Agnes API** (`backend/`)
A high-performance REST API built with FastAPI and Python 3.11+ that serves as the data backbone for the entire Agnes ecosystem. It provides:
- 📡 IoT device and sensor management
- 📊 Real-time data collection and readings
- 🗺️ Location-based farm organization
- 📁 Category management for devices and data
- 👥 User authentication and authorization
- ❤️ Health monitoring endpoints

**Tech Stack:**
- FastAPI 0.135.1
- Pydantic 2.12.5 (with v2 validation)
- SQLAlchemy 2.0.48
- PostgreSQL (via pg8000)
- Alembic for migrations
- Python Spartan CLI

[📖 View API Documentation](backend/README.md)

### 🎨 Frontend Applications

#### **Agnes Web App** (`frontend/`)
Modern, responsive web interface built with Next.js for managing farm operations. Provides an intuitive dashboard for monitoring devices, viewing sensor data, and managing farm resources.

**Tech Stack:**
- Next.js (React framework)
- TypeScript
- Tailwind CSS (PostCSS)

[📖 View Web App Documentation](frontend/README.md)

### 🚧 Planned Components

#### **Agnes CLI**
Command-line interface tools for developers and system administrators to interact with the Agnes platform directly from the terminal.

#### **Agnes Workflow (n8n)**
Automated workflow orchestration using n8n for handling background processing, scheduled tasks, data synchronization, and integration with third-party services in farm operations.

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
   cd backend
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

4. **Run the API development server**
   ```bash
   spartan serve
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Getting Started with the Web App

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

   The web app will be available at `http://localhost:3000`

## 🧪 Testing

### Backend API Tests

Run tests for the API service:

```bash
cd backend
pytest
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📚 Documentation

- [API Documentation](backend/README.md)
- [API Reference](http://localhost:8000/docs) (when running locally)
- [Web App Documentation](frontend/README.md)
- [Changelog](backend/CHANGELOG.md)
- [Contributing Guidelines](backend/CONTRIBUTING.md)
- [Code of Conduct](backend/CODE_OF_CONDUCT.md)

## 🛠️ Technology Stack

### Backend (Agnes API)
- **Framework:** FastAPI 0.135.1
- **Language:** Python 3.11+
- **Database:** PostgreSQL with SQLAlchemy 2.0.48 ORM
- **Validation:** Pydantic 2.12.5
- **Migrations:** Alembic 1.18.4
- **CLI Tool:** Python Spartan 0.3.9
- **Testing:** pytest

### Frontend (Agnes Web App)
- **Framework:** Next.js
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Build Tool:** PostCSS

### Orchestration (Planned)
- **Workflow Engine:** n8n
- **Purpose:** Automated workflows, background processing, integrations

### Key Features
- ✅ RESTful API architecture
- ✅ Pydantic v2 data validation
- ✅ Database migrations with Alembic
- ✅ Comprehensive test coverage
- ✅ Modern responsive web interface
- ✅ FastAPI automatic API documentation
- ✅ CORS middleware for web clients
- ✅ Environment-based configuration
- ✅ TypeScript for type safety
- 🚧 CLI tools (coming soon)
- 🚧 n8n workflow automation (coming soon)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](backend/CONTRIBUTING.md) for details on:

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

**Note:** Agnes is actively developed and maintained. For the latest updates, check the [Changelog](backend/CHANGELOG.md).
