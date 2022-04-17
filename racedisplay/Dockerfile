# Generic Poetry Build Stage
FROM python:3.9.7-slim as builder
RUN pip3 install "poetry==1.1.11"

# copy and build service to Wheel
WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY ./racedisplay ./racedisplay
RUN poetry build

# build the actual image with just Python + PIP
FROM tiangolo/uvicorn-gunicorn:python3.8-slim
COPY --from=builder /app/dist/racedisplay*.whl ./whl/
RUN pip3 install ./whl/*

# run service with uvicorn
EXPOSE 8000
ENTRYPOINT [ "uvicorn", "racedisplay.main:app", "--host", "0.0.0.0", "--port", "8000" ]
