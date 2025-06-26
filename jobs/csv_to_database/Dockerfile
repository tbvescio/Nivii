FROM python:3.9
WORKDIR /app
COPY import_csv_to_postgres.py ./
COPY data.csv ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "import_csv_to_postgres.py"] 