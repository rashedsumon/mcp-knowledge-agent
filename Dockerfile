# Use an explicit, highly stable Python slim image to ensure 
# 100% compatibility with CrewAI, Pydantic v1, and ChromaDB.
FROM python:3.11-slim

# Set system environment optimizations
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for compiling heavy Python binaries (like FAISS or Torch)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker's layer caching mechanism
COPY requirements.txt .

# Upgrade pip and install dependencies cleanly
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