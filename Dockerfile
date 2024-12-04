FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    git \
    libpq-dev \
    portaudio19-dev \
    ffmpeg \
    libc-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

COPY server.py /code/server.py
COPY utils /code/utils

CMD ["python", "server.py"]