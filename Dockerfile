FROM python:3.9.0

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# copy source files
COPY . /usr/src/app

# install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000/tcp

# run server
CMD ["python", "app.py"]
