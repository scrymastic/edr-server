
echo "Starting EDR Server..."

python /usr/src/app/manage.py migrate

exec "$@"