# syntax=docker/dockerfile:1

# Use Python as the base image, bookworm is a Docker image and inside the container it will be Python 3.12.5
FROM python:3.12.5-bookworm

# Set the working directory to /contrans2024
WORKDIR /contrans2024

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install pip3
RUN pip3 install --upgrade pip

# Install all packages from requirements.txt using pip
RUN pip3 install -r requirements.txt

# Expose the port for the dashboard
EXPOSE 8050

# Run the dashboard when the container starts
CMD ["python", "app.py"]