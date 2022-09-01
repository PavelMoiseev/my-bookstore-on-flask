FROM python:3.10.4
COPY . /app
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]