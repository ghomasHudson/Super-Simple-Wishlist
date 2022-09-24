FROM python:3.9.0

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# copy source files
COPY . /usr/src/app

# install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# setup env
ENV PYTHONUNBUFFERED=1

# run server
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--with-threads"]
