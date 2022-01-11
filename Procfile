web: gunicorn shelix.asgi:application -k uvicorn.workers.UvicornWorker -c gconfig.py
worker: python manage.py run_huey
