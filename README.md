# Django + PostgreSQL Docker starter

## Requirements
- Docker Desktop (or Docker Engine with the Compose plugin)

## Start the stack
```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open http://localhost:8000/

## First-time setup
This starter includes Docker and PostgreSQL configuration, but not a generated Django project.
Create the project files in this directory before starting the web container:

```bash
docker compose run --rm web django-admin startproject config .
docker compose up --build -d
docker compose exec web python manage.py migrate
```

The database credentials are in `.env`. Change the sample `SECRET_KEY` and passwords before using this beyond local development.

## Stop
```bash
docker compose down
```

To remove the database volume too (this permanently deletes stored database data):
```bash
docker compose down -v
```
