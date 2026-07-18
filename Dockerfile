FROM python:3.10-slim
WORKDIR /app
COPY server/ /app/server/
COPY data/ /app/data/
EXPOSE 5555
ENV PYTHONUNBUFFERED=1
CMD ["python", "server/main.py"]
