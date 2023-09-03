
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Ports should be separated by commas
# Change "--port" to "-p"
# Comment out the incorrect EXPOSE command
# Add CMD command to run the application
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "-p", "8000"]
