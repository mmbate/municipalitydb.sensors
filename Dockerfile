# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt


# Copy the rest of the application code into the container
COPY . /app


# Define the command to run the application when the container starts
CMD ["python3", "main.py"]
