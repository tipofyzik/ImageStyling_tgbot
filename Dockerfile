FROM python:3.11-slim-bullseye

# ENV PIP_FIND_LINKS="https://download.pytorch.org/whl/torch_stable.html"

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt
RUN pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip cache purge

WORKDIR /app/tgbot
COPY tgbot .

CMD ["python", "app.py"]
