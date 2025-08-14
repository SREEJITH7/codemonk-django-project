# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first (to cache pip installs)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Expose Django default port
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
