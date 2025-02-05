# Description: Dockerfile to build a docker image for the DECIMER Servers
# Since linux kernel based, no mac-gpu support unfortunately
FROM python:3.11.9-slim
RUN apt-get update && \
    apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app and copy all the files (requirements.txt, decimerapiapp.py, decimer_ic) to /app
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt
# add the adapted decimer image classifier and decimerapi packages
# RUN python -m pip install /app/packages/decimer_ic

# To avoid redownloading the model every time the container is started; needs mounting when running the container
RUN mkdir -p /home/appuser/.data/DECIMER-V2

# Add a non-root user to run the app
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chown -R appuser:appuser /home/appuser/.data
USER appuser

# open port to listen to requests from outside
EXPOSE 8099

# Define environment variable
ENV NAME=app

# Run decimerapiapp.py when the container launches
CMD ["python", "decimer_server.py"]