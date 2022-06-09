FROM arm64v8/python:3.10.4-bullseye
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
ENV STREAMLIT_SERVER_PORT=8080

CMD ["streamlit", "run", "app.py"]
