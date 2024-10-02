FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pwd
RUN ls -al
CMD ["python","src/main.py"]