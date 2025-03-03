# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Force Python to print logs immediately
ENV PYTHONUNBUFFERED=1

# Expose ports (HTTP and WebSocket)
EXPOSE 8000 5555

# Command to run the server
CMD ["python", "server.py"]
