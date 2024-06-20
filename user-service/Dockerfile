# Use an official Python runtime as a parent image
FROM python:3.12

LABEL maintainer="bilalraza"

# Set the working directory in the container
WORKDIR /code

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    protobuf-compiler \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /code
COPY ./pyproject.toml /code/

# Configuration to avoid creating virtual environments inside the Docker container
RUN poetry config virtualenvs.create false

# Install dependencies including development ones
RUN poetry install

COPY . /code/

# Make port 8000 available to the world outside this container
EXPOSE 8081

# Run the app. CMD can be overridden when starting the container
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0","--port", "8081", "--reload"]