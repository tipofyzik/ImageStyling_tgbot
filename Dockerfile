FROM python:3.11-slim-bullseye

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir
RUN pip cache purge

WORKDIR /app/tgbot
COPY tgbot .

CMD ["python", "app.py"]
