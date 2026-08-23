FROM python:3.10-slim

RUN groupadd --system appgroup && useradd --system --group appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chown -R root:root /app

# USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
