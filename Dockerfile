# Description: Dockerfile to build a docker image for the DECIMER Servers
# Since linux kernel based, no mac-gpu support unfortunately
#
# A two stage builder leading to a nearly 18% reduced image size, but a bit more complex.
# Could potentially be optimized even further?
#
## -------- Production Stage ----------##
FROM python:3.11.9-slim-bullseye AS builder

RUN apt-get update && apt-get install -y\
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory to /app and copy all the files (requirements.txt, decimerapiapp.py, decimer_ic) to /app
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt
RUN rm -rf /app/packages

## -------- Production Stage ----------##
FROM python:3.11.9-slim-bullseye AS production
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

# Verify the installation of the packages
RUN python -m pip list

# Run decimer_server.py when the container launches
CMD ["python", "decimer_server.py"]
