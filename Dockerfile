FROM python:alpine3.7 
COPY . /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
COPY app.py /app
EXPOSE 5001 
CMD ["python", "app.py" ] 