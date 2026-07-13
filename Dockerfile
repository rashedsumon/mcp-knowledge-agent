# Switch to the full official Python image. 
# This image already contains build-essential, curl, and git pre-installed.
FROM python:3.11

# Set system environment optimizations
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Set the working directory inside the container
WORKDIR /app

# No apt-get commands needed here anymore! This prevents the status 100 error entirely.

# Copy requirements first to leverage Docker's layer caching mechanism
COPY requirements.txt .

# Upgrade pip and install your dependencies cleanly
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application codebase into the container
COPY . .

# Expose the default port used by Google Cloud Run
EXPOSE 8080

# Configure Streamlit specific production flags
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# Run Streamlit, binding it to the port defined by Google Cloud's environment
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]