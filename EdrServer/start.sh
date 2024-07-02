
echo "Starting EDR Server..."

python3 /usr/src/app/manage.py migrate

exec "$@"