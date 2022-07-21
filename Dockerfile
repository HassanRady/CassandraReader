FROM python:slim


# set work directory
WORKDIR /cassandra-reader

# ENV CASSANDRA_HOST=cassandra
# ENV CASSANDRA_PORT=9042
# ENV KEYSPACE=twitter
# ENV TABLE=offline_tweets

# install dependencies
# RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# EXPOSE 9015

COPY . /cassandra-reader


# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9015"]