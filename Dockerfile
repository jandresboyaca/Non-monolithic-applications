FROM python:3.9-slim-buster as base
WORKDIR /app

COPY . .

FROM base as service1
RUN pip install -r service1/requirements.txt
CMD ["python", "service1/main.py"]

FROM base as service2
RUN pip install -r service2/requirements.txt
CMD ["python", "service2/main.py"]

FROM base as service3
RUN pip install -r service3/requirements.txt
CMD ["python", "service3/main.py"]

FROM base as service4
RUN pip install -r service4/requirements.txt
CMD ["python", "service4/main.py"]

EXPOSE 8080
