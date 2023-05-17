# Generic Poetry Build Stage
FROM arm64v8/python:3.10.4-bullseye as builder
RUN pip3 install "poetry==1.1.11"

# copy and build service to Wheel
WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY ./driftapi ./driftapi
RUN poetry build


# build the actual image with just Python + PIP
# FROM tiangolo/uvicorn-gunicorn:python3.8
FROM tedivm/uvicorn-gunicorn:latest
COPY --from=builder /app/dist/driftapi*.whl ./whl/
RUN pip3 install ./whl/*

# run service with uvicorn
EXPOSE 8001
ENTRYPOINT [ "uvicorn", "driftapi.main:app", "--host", "0.0.0.0", "--port", "8001" ]
