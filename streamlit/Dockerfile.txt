FROM python:3.7
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . ./app
ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]