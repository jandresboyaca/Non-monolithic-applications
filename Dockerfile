FROM python:3.10.6-slim-buster AS base
WORKDIR /app

COPY . .
RUN pip3 install --upgrade pip

FROM base as service1
RUN pip install -r order/requirements.txt --compile --no-cache-dir
CMD ["/bin/bash", "-c", "python order/main.py & python order/main2.py;tail -f /dev/null"]

FROM base as service2
RUN pip install -r client/requirements.txt --compile --no-cache-dir
CMD ["python", "client/main.py"]

FROM base as reporting
RUN pip install -r reporting/requirements.txt --compile --no-cache-dir
CMD ["/bin/bash", "-c", "python reporting/main.py & python reporting/api.py;tail -f /dev/null"]

FROM base as service4
RUN pip install -r pagos/requirements.txt --compile --no-cache-dir
CMD ["python", "pagos/main.py"]

FROM base as saga_log
RUN pip install -r saga_log/requirements.txt --compile --no-cache-dir
CMD ["python", "saga_log/main.py"]


FROM base as bff
RUN pip install -r bff/requirements.txt --compile --no-cache-dir
CMD ["python", "bff/main.py"]

EXPOSE 8080
