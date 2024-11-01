# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install necessary Python packages
RUN pip install --no-cache-dir requests beautifulsoup4 mysql-connector-python

# Environment variables for MySQL connection (optional, for example purposes)
ENV MYSQL_HOST=localhost
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=your_password
ENV MYSQL_DB=property_data

# Command to run the scraper script
CMD ["python", "app.py"]
