# Dockerfile for Streamlit app
# This Dockerfile sets up a Streamlit application using Python 3.11-slim as the base image. It installs the required dependencies from requirements.txt, copies the application code, and exposes port 8501 for the Streamlit server.

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
