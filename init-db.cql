
CREATE KEYSPACE twitter
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};

USE twitter;

create table offline_tweets
(
    id    uuid primary key,
    text  text,
    author_id text,
    topic text
);

insert into offline_tweets (id, text, author_id, topic) values (uuid(), 'hello there', '1', 'test');
