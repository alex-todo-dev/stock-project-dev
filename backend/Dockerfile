FROM python:3.11-slim

WORKDIR /app

# Install cron and required utilities
RUN apt-get update && apt-get install -y cron procps

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Copy cron job file into container
COPY scheduler.cron /etc/cron.d/my-cron-job

# Fix permissions and load the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job \
    && crontab /etc/cron.d/my-cron-job

# Create log file
RUN touch /var/log/cron.log

EXPOSE 5000

# Run cron in background, then Flask, and keep container alive
CMD ["sh", "-c", "cron && python app.py & tail -f /var/log/cron.log"]
