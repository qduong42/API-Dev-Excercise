FROM python:3.80-alpine

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN python3 dataReceiveStoreEnv.py

CMD ["python3", "mainEnv.py"]