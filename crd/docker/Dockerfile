FROM python:3.11-slim
WORKDIR /app
COPY cake_controller.py .
RUN pip install kopf kubernetes
CMD ["kopf", "run", "--standalone", "--namespace=studentx", "/app/cake_controller.py"]
