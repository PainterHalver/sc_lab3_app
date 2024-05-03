#!/bin/sh

# Check if the EC2 instance metadata service exists
STATUS_CODE=$(curl -o /dev/null -w "%{http_code}" -s http://169.254.169.254/latest/meta-data/instance-id)
if [ $STATUS_CODE -eq 200 ]; then
  # If it exists, get the instance ID
  INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

  # Replace the placeholder in the static files with the instance ID
  find /app/client/build -name "*.js" -exec sed -i -e "s/INSTANCE_ID/${INSTANCE_ID}/g" {} \;
fi

# Start the gunicorn server
gunicorn --bind 0.0.0.0:8080 "app:create_app()" --workers 3 --threads 12 --access-logfile /var/log/app-access.log --error-logfile /var/log/app-error.log
