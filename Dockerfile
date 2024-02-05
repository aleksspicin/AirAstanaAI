
FROM python:3.11
COPY requirements.txt .
ADD . AirAstana/
WORKDIR AirAstana/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD main run

ENTRYPOINT ["python", "main.py"]