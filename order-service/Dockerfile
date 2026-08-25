FROM python:3.10-slim

#Fix 1 : --gid and appgroup not given which tells that to which group appuser belongs.
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

#Fix 2 : root:root gives all root permissions and there is no use of making addgroup and appuser then.
RUN chown -R root:root /app

# Fix 3 : USER appuser is commented, we have to uncomment it so the application do not run as ROOT user.
USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
