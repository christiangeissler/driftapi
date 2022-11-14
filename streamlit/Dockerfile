FROM python:3.9.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
ENV STREAMLIT_SERVER_PORT=8080

CMD ["streamlit", "run", "app.py"]
