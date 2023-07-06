FROM python:3.11-slim-bullseye

WORKDIR /app/tgbot
COPY tgbot .

WORKDIR /app

COPY app.py .
COPY API.txt .
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN pip cache purge

CMD ["python", "app.py"]
