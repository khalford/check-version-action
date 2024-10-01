FROM python:3
WORKDIR /app
COPY . .
RUN pip instal -r requirements.txt
CMD ["main.py"]