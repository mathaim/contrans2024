# syntax=docker/dockerfile:1

# Use Python as the base image
FROM python:3.12.5-bookworm

# Set the working directory to /contrans2024
WORKDIR /contrans2024

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt

# Install pip3
RUN pip3 install --upgrade pip

# Install all packages from requirements.txt using pip
RUN pip3 install -r requirements.txt

# Expose the port for Jupyter Lab
EXPOSE 8888

# Run Jupyter Lab when the container starts
CMD ["jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--port=8888"]