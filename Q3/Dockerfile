FROM python:3.10-slim
WORKDIR /app
RUN pip install pandas
COPY validate.py .
CMD ["python", "validate.py"]
