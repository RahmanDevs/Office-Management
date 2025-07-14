find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -type d -name "__pycache__" -exec rm -r {} +
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('root', 'admin@example.com', 'admin')"