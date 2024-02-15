FROM python:latest

COPY backend/ .

RUN pip install --no-cache-dir -r requirements.txt

# RUN python3 dataReceiveStoreEnv.py

# CMD ["python3", "mainEnv.py"]
ENTRYPOINT [ "tail" ]
CMD ["-f", "/dev/null"]