FROM python:3.11.3

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app/tgbot
COPY tgbot .

CMD ["python", "app.py"]
