FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Ports should be separated by commas
# Change "--port" to "-p"
EXPOSE 8000
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "-p", "0"]