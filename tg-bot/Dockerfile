FROM python:slim

WORKDIR /tg-bot

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "ccourseproject_bot"]


#  tg-bot:
#    build:
#      context: tg-bot
#      dockerfile: Dockerfile
#    container_name: tg-bot
#    depends_on:
#      - problem-solver
#      - web
#      - py-sc-server
#      - nika-ui
#    restart: unless-stopped
#    networks:
#      - nika