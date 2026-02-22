# Description: Dockerfile to build a docker image for the DECIMER Servers
# Since linux kernel based, no mac-gpu support unfortunately
#
## -------- Production Stage ----------##
FROM python:3.10-slim-bullseye AS builder

RUN apt-get update && apt-get install -y\
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app and copy all the files
WORKDIR /app
COPY . /app

# Install via uv workspace; --no-editable copies package files into venv so source can be removed
# UV_PYTHON_PREFERENCE=only-system forces uv to use the container's Python rather than downloading
# its own, which would break venv symlinks in the production stage.
RUN pip install uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_PYTHON_PREFERENCE=only-system
ENV PATH="/opt/venv/bin:$PATH"
RUN uv sync --no-dev --no-editable

# Verify the installation of the packages
RUN uv pip list
RUN rm -rf /app/packages

## -------- Production Stage ----------##
FROM python:3.10-slim-bullseye AS production
RUN apt-get update && apt-get install -y\
    libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# To avoid redownloading the model every time the container is started; needs mounting when running the container
RUN mkdir -p /home/appuser/.data/DECIMER-V2

# Copy the application files from the builder stage
COPY --from=builder /app /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory to /app
WORKDIR /app

# Add a non-root user to run the app
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chown -R appuser:appuser /home/appuser/.data
USER appuser

# open port to listen to requests from outside
EXPOSE 8099

# Define environment variable
ENV NAME=app
ENV PYTHONPATH=/app

# Run decimer_server.py when the container launches
CMD ["python", "decimer_server.py"]
