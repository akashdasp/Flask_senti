# syntax=docker/dockerfile:1
FROM python:3.9

# Create app directory
WORKDIR /senti

# Install app dependencies
COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 5000
CMD ["python3", "-m" ,"flask", "run","--host","0.0.0.0","--port","5000"]