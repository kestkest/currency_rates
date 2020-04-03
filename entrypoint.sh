python manage.py migrate
python manage.py populate_currency_table
python manage.py initadmin
gunicorn --workers=2 --threads=4 --log-level debug --timeout 90 --bind=0.0.0.0:8000 currency_rates.wsgi:application --reload