FROM python:3.10.6-slim-buster AS base
WORKDIR /app

COPY . .
RUN pip3 install --upgrade pip

FROM base as service1
RUN pip install -r order/requirements.txt --compile --no-cache-dir
CMD ["python", "order/main.py"]

FROM base as service2
RUN pip install -r client/requirements.txt --compile --no-cache-dir
CMD ["python", "client/main.py"]

FROM base as reporting
RUN pip install -r service3/requirements.txt --compile --no-cache-dir
CMD ["python", "reporting/main.py"]

FROM base as service4
RUN pip install -r service4/requirements.txt --compile --no-cache-dir
CMD ["python", "service4/main.py"]

EXPOSE 8080
