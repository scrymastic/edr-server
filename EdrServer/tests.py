
from datetime import datetime

# Assume this is your datetime string
datetime_str = '2024-06-14T08:02:52.143988+00:00'

# Convert the string back to a datetime object
dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')

print(dt)