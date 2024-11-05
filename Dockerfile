FROM python:3

WORKDIR /app

COPY ./app.py /app/app.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y nano vim

CMD ["python", "app.py"]
