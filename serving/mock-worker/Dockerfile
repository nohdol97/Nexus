FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

ENV HOST=0.0.0.0
ENV PORT=8001

CMD ["sh", "-c", "uvicorn app:app --host ${HOST} --port ${PORT}"]
