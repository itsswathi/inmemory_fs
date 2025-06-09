# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements*.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Install package in development mode
RUN pip install -e .

# Run tests on build, fail if any tests fail
RUN python3 -m pytest -vv tests/

# Set working directory to root for filesystem operations
WORKDIR /

# Create a non-root user for better security
RUN useradd -m fsuser
USER fsuser

# Start an interactive shell by default
CMD ["/bin/bash"] 