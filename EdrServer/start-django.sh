
#!/bin/bash

echo 'Setting up EDR Server...'
cd /usr/src/app
python3 manage.py makemigrations
python3 manage.py migrate

export DJANGO_SUPERUSER_USERNAME='kali'
export DJANGO_SUPERUSER_EMAIL='kali@example.com'
export DJANGO_SUPERUSER_PASSWORD='kali'

# Attempt to create the superuser and suppress the 'already exists' error
if python3 manage.py createsuperuser --noinput; then
    echo "Superuser created."
else
    echo "Superuser already exists or could not be created."
fi
echo 'EDR Server is set up.'

python3 manage.py runserver 0.0.0.0:8001
