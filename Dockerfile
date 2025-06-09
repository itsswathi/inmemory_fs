# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy all Python files and README
COPY *.py /app/
COPY README.md /app/

# Make the Python scripts executable
RUN chmod +x /app/filesys.py /app/permissions.py

# Create symlinks in /usr/local/bin for easy access
RUN ln -s /app/filesys.py /usr/local/bin/fs && \
    ln -s /app/permissions.py /usr/local/bin/perms

# Create a non-root user to run the application
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Add /usr/local/bin to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Default command (can be overridden)
CMD ["bash"] 