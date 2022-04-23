import pymysql
from contextlib import closing


class Database:
    def __init__(self, host, user, password, db_name):
        conn = pymysql.connect(
            host=host,
            user=user, passwd=password,
            db=db_name,
            connect_timeout=5,
            autocommit=True)
        conn.ping(reconnect=True)
        conn.begin()

        self.connection = conn

    def get_all_channels(self):
        with closing(self.connection.cursor()) as cur:
            cur.execute('SELECT name FROM channel')
            channels = cur.fetchall()
        return [name.lower() for name, in channels]

    def get_daily_content_reserve_days(self):
        with closing(self.connection.cursor()) as cur:
            cur.execute('SELECT daily_content_reserve_date FROM system_config WHERE id = 1')
            reserve_days, = cur.fetchone()

        return reserve_days
