# Start up an app on :2137
# pipenv run uvicorn app.main:app --reload --port 2137
DJANGO_SETTINGS_MODULE=app.settings python app/manage.py runserver 2137
