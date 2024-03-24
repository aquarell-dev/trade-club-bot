FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./ /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]