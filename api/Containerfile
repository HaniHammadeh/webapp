# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install necessary Python packages
RUN pip install --no-cache-dir requests beautifulsoup4 mysql-connector-python Flask

# Environment variables for MySQL connection (optional)
ENV MYSQL_HOST=localhost
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=your_password
ENV MYSQL_DB=property_data

# Expose port for Flask API
EXPOSE 5000

# Command to run the API
CMD ["python", "api_app.py"]
