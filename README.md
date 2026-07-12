# EcoSphere: ESG Management Platform

EcoSphere is a web-based ESG (Environmental, Social, and Governance) management platform built by Team NASA Hackers. It helps organizations manage sustainability initiatives, monitor ESG performance, encourage employee participation, and generate reports from a single platform.

The project was developed as part of a hackathon with the goal of providing a practical and scalable solution for enterprise ESG management.

---

## Team

- Neevan Redkar – https://github.com/Neevs1
- Pranav Ijantkar – https://github.com/Pranav-Ijantkar
- Prerana Pawar – https://github.com/PreranaPawar10
- Gayatri Apte – https://github.com/gayatri-apte

---

## Features

- Secure authentication with JWT
- Role-based access control
- Centralized ESG dashboard
- Environmental monitoring and carbon tracking
- CSR activity management
- Governance and compliance tracking
- Employee gamification through challenges and rewards
- ESG reporting with CSV export
- Department and ESG configuration management

---

## Tech Stack

### Frontend

- React (Vite)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Zustand
- TanStack Query
- Axios

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib

### Database

- PostgreSQL

### Development

- Docker
- Docker Compose

---

## Project Structure

```
backend/
├── app/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py

frontend/
└── app/
    └── ecosphere/
        ├── src/
        │   ├── api/
        │   ├── components/
        │   ├── pages/
        │   ├── store/
        │   └── lib/
```

---

## Development Approach

We divided the project into multiple development sprints, following an Agile-style workflow.

The backend and frontend were developed in parallel, allowing each module to be built and integrated independently. Authentication and the project foundation were implemented first, followed by the Environmental, Social, Governance, Gamification, Reporting, and Settings modules.

The backend follows a layered architecture:

```
Frontend
    ↓
REST API
    ↓
Pydantic Schemas
    ↓
Routers
    ↓
Services / CRUD
    ↓
SQLAlchemy Models
    ↓
PostgreSQL
```

This separation keeps the codebase modular and makes it easier to maintain and extend.

---

## Running the Project

Clone the repository and start the application using Docker.

```bash
docker compose up --build
```

Once the containers are running:

Frontend

```
http://localhost:5173
```

Backend

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## API Documentation

FastAPI automatically generates interactive API documentation, making it easy to test and explore every endpoint during development.

```
http://localhost:8000/docs
```

---

## Future Scope

Some areas we would like to expand include:

- Real-time notifications
- AI-powered sustainability insights
- Advanced analytics and forecasting
- Integration with external ERP systems
- Mobile application support

---

## About EcoSphere

EcoSphere was built with the idea of bringing Environmental, Social, and Governance management into one unified platform. Instead of relying on multiple disconnected tools, organizations can monitor their ESG initiatives, track progress, manage departments, and generate reports through a single interface.
