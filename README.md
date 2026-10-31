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
3. Startup runs `python manage.py migrate`; migrations are committed to Git. If you change a model, run `docker compose exec auth_service python manage.py makemigrations <app>`, commit the new migration file, then `docker compose up` again.
4. Check `http://localhost:8001/api/health/`.

## Start Patient Service
The same `docker compose up --build` also starts `patient_db` and `patient_service`.
1. Check `http://localhost:8002/api/health/`.
2. Log in through the auth service to get a JWT — tokens carry `role`, `username`, and `user_id` claims, and both services share `DJANGO_SECRET_KEY`, so the patient service validates tokens offline without calling auth.
3. Endpoints (all under `/api/`):

| Endpoint | Access |
|---|---|
| `GET patients/` | staff (admin/doctor/receptionist); `?search=`, `?auth_user_id=`, `?include_inactive=true` |
| `POST patients/` | staff; medical record number is auto-generated |
| `GET patients/{id}/` | staff, or the owning patient |
| `PATCH patients/{id}/` | staff |
| `GET patients/me/` | patient; the profile linked to `auth_user_id` |
| `POST patients/{id}/deactivate/` | admin or receptionist (soft delete) |

4. Run its tests:
```powershell
docker compose exec patient_service python manage.py test patients
docker compose exec auth_service python manage.py test accounts
```

## API documentation
Both services expose an OpenAPI 3 schema and interactive docs. They are routed only when `API_DOCS_ENABLED=1` (defaults to the value of `DJANGO_DEBUG`):

| Service | Swagger UI | ReDoc | Raw schema |
|---|---|---|---|
| Auth | `http://localhost:8001/api/docs/` | `http://localhost:8001/api/docs/redoc/` | `http://localhost:8001/api/schema/` |
| Patient | `http://localhost:8002/api/docs/` | `http://localhost:8002/api/docs/redoc/` | `http://localhost:8002/api/schema/` |

Calling protected endpoints from Swagger UI:
1. `POST /api/auth/token/` on port 8001 with `{"username": "...", "password": "..."}`.
2. Copy the `access` value (not `refresh`).
3. Click **Authorize** on either docs page, paste the token without the `Bearer ` prefix, then Authorize.
4. Access tokens expire after 15 minutes; get a new one with `POST /api/auth/token/refresh/`.

### If you get 401 on /api/patients/
Opening an API URL directly in a browser cannot work: browsers do not send an `Authorization` header, and the patient service has no local users to log in as. Use one of these:

```powershell
$login = Invoke-RestMethod -Method Post -Uri http://localhost:8001/api/auth/token/ `
  -ContentType 'application/json' -Body '{"username":"<user>","password":"<password>"}'
Invoke-RestMethod -Uri http://localhost:8002/api/patients/ `
  -Headers @{ Authorization = "Bearer $($login.access)" }
```
- or Swagger UI at `http://localhost:8002/api/docs/` (Authorize remembers the token, but only on that page — authorizing on the auth docs does not carry over to the patient docs).
- Use the `access` token, not `refresh`, and paste without the `Bearer ` prefix in Swagger.
- Keep the trailing slash; `/api/patients` only redirects (301) and some clients drop the auth header on redirect.

Export the schema (for a frontend client or contract checks) and validate it:
```powershell
docker compose exec auth_service python manage.py spectacular --file schema.yml --validate
docker compose exec patient_service python manage.py spectacular --file schema.yml --validate
```

Useful commands:
```powershell
docker compose ps
docker compose logs -f auth_service
docker compose logs -f patient_service
docker compose exec auth_service python manage.py check
docker compose exec patient_service python manage.py check
docker compose exec auth_service python manage.py migrate
docker compose exec patient_service python manage.py migrate
docker compose down
```

Never commit `.env`, production secrets, or real patient data.
