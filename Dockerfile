FROM python:3.12

WORKDIR /app

ADD requirements.txt .

RUN pip3 install -r requirements.txt

ADD . .

CMD ["python3", "-m", "char_sheets.main"]
