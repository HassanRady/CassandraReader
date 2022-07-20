from cassandra.cluster import Cluster
import os
from cassandra.auth import PlainTextAuthProvider


class CassandraDriver:
    def __init__(self, HOST, PORT, KEYSPACE) -> None:
        auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')
        self.cluster = Cluster([HOST], port=PORT, auth_provider=auth_provider)
        self.session = self.cluster.connect(KEYSPACE)

    def get_all_data(self, TABLE):
        return self.session.execute('SELECT * FROM {}'.format(TABLE))


if __name__ == "__main__":
    cd = CassandraDriver(os.environ.get('CASSANDRA_HOST', '0.0.0.0'), os.environ.get('CASSANDRA_PORT', 9042), os.environ.get('KEYSPACE', 'twitter'))
    rows = cd.get_all_data('offline_tweets')
    for row in rows:
        print(row.text)


