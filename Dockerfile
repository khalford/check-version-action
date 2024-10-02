FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pwd
RUN ls -la
CMD ["python","/app/src/main.py"]