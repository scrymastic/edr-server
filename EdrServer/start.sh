
echo "Setting up EDR Server..."

export DJANGO_SUPERUSER_USERNAME=kali
export DJANGO_SUPERUSER_EMAIL=kali@example.com
export DJANGO_SUPERUSER_PASSWORD=kali
python3 /usr/src/app/manage.py createsuperuser --noinput
python3 /usr/src/app/manage.py migrate

echo "EDR Server is set up."

exec "$@"
