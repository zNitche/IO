python manage.py makemigrations --no-input
python manage.py migrate --no-input

gunicorn -c gunicorn.conf.py io_app.wsgi --preload
