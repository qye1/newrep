FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir keyboard

CMD ["python", "your_script.py"]
