FROM debian:latest
RUN apt-get update -y
RUN apt-get install -y \
    python3-pip python3.11-venv python3-dev build-essential libssl-dev libffi-dev \
    libpq-dev libjpeg-dev zlib1g-dev
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Set the shell script as the entrypoint
CMD ["python3", "main.py"]
