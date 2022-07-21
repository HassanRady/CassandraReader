from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraDriver:
    def __init__(self, HOST, PORT, KEYSPACE) -> None:
        auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')
        self.cluster = Cluster([HOST], port=int(PORT), auth_provider=auth_provider)
        self.session = self.cluster.connect()
        keyspace_strategy = {'class': 'SimpleStrategy', 'replication_factor': 1}
        self.session.execute(f"create KEYSPACE IF NOT EXISTS {KEYSPACE} WITH REPLICATION = {keyspace_strategy}")
        self.session.set_keyspace(KEYSPACE)

        OFFLINE_TABLE = os.environ['OFFLINE_TABLE']
        ONLINE_TABLE = os.environ['ONLINE_TABLE']

        self.session.execute(f"create TABLE IF NOT EXISTS {OFFLINE_TABLE} (id text, text text, author_id text, topic text, PRIMARY KEY (id))")
        self.session.execute(f"create TABLE IF NOT EXISTS {ONLINE_TABLE} (id text, text text, author_id text, topic text, PRIMARY KEY (id))")

        prepared = self.session.prepare(f"INSERT INTO {OFFLINE_TABLE} (id, author_id, text, topic) VALUES (?, ?, ?, ?)")
        with open('data/offline_tweets.csv', 'r') as f:
            for line in f:
                id, text, author_id, topic = line.split(',')
                self.session.execute(prepared, (id, text, author_id, topic))


    def get_all_data(self, TABLE):
        data = self.session.execute('SELECT * FROM {}'.format(TABLE))
        return data


if __name__ == "__main__":
    import os
    cd = CassandraDriver(os.environ.get('CASSANDRA_HOST', '0.0.0.0'), os.environ.get('CASSANDRA_PORT', 9042), os.environ.get('KEYSPACE', 'twitter'))
    rows = cd.get_all_data('offline_tweets')
    for row in rows:
        print(row.text)


