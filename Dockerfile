# Use a smaller, security-focused Python image (alpine-based)
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install dependencies (if needed for specific packages)
RUN pip install --upgrade pip

# Set environment variable to avoid Python buffering issues
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
