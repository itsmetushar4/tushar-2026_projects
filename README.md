# Hospital Management System — Microservices

Interview-focused full-stack project using React, Django REST Framework, PostgreSQL, Docker, Nginx, and Celery/Redis.

## Architecture
- React frontend: authentication, patients, doctors, appointments, billing.
- Nginx gateway: public API entry point and routing.
- Auth Service: users, roles, JWT.
- Patient Service: patient profiles.
- Appointment Service: doctors, availability, appointments, clinical records.
- Billing Service: invoices and payments.
- Notification worker: asynchronous notifications and event processing.
- Each business service owns its own PostgreSQL database.

## Architecture rules
1. Services own their models, migrations, and databases.
2. Never query another service's database directly.
3. Use HTTP APIs for immediate requests and events for asynchronous workflows.
4. Every service enforces authorization.
5. Use database constraints for invariants such as appointment conflicts.
6. Use idempotency, bounded retries, and an outbox for reliable cross-service workflows.

## Start Auth Service
1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Compose creates the initial custom-user migration and applies migrations during startup. If you later change models, run `docker compose exec auth_service python manage.py makemigrations` followed by `docker compose exec auth_service python manage.py migrate`.
4. Check `http://localhost:8001/api/health/`.

Useful commands:
```powershell
docker compose ps
docker compose logs -f auth_service
docker compose exec auth_service python manage.py check
docker compose exec auth_service python manage.py migrate
docker compose down
```

Never commit `.env`, production secrets, or real patient data.
