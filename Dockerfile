FROM python:3
COPY . .
RUN pip install -r requirements.txt
RUN pwd
RUN ls -la
CMD ["python","src/main.py"]