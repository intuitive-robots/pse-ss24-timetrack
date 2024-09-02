FROM python:3.12-slim
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5001", "app:app", "--preload"]