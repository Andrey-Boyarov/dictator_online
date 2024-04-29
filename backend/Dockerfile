FROM python:3.10.14-alpine3.19

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./*.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]