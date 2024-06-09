# Use Ubuntu as the base image
FROM ubuntu:20.04

# Update package list and install required dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /app
COPY . /src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000
ENV PYTHONPATH=/src

# Define the command to run your FastAPI server when the container starts
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "run", "main.py", "--port", "8000"]
# CMD ["gunicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["python3", "main.py"]
