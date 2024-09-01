FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r req.txt

CMD python src/main.py