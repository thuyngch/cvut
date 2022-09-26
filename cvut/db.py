import uuid
import psycopg2
from psycopg2.extras import execute_values


__all__ = ['PostgreSQLDatabase', ]


class PostgreSQLDatabase(object):

    def __init__(self, user, password, host, port, db_name, table_name):
        self.table_name = table_name
        self.conn = psycopg2.connect(host=host, port=port,
                                     user=user, password=password,
                                     database=db_name)

    def get_uuid(self, ):
        id = str(uuid.uuid4())
        return id

    def check_record_existed(self, limit1=True, **kwargs):
        cursor = self.conn.cursor()
        cmd = f"""
        SELECT exists (
            SELECT 1 FROM {self.table_name} WHERE
        """
        for idx, (key, val) in enumerate(kwargs.items()):
            if idx != 0:
                cmd += " AND "
            cmd += f"{key} = '{val}'"
        if limit1:
            cmd += f" LIMIT 1"
        cmd += ");"
        cursor.execute(cmd)
        existed = cursor.fetchone()[0]
        cursor.close()
        return existed

    def insert_record(self, **kwargs):
        cursor = self.conn.cursor()
        keys = list(kwargs.keys())
        vals = list(kwargs.values())
        cmd = f"INSERT INTO {self.table_name} ({', '.join(keys)}) VALUES %s"
        execute_values(cursor, cmd, [vals])
        self.conn.commit()
        cursor.close()

    def get_records(self):
        cursor = self.conn.cursor()
        cmd = f"SELECT * FROM {self.table_name} ORDER BY time"
        cursor.execute(cmd)
        records = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        return records, colnames

    def update_record(self, **kwargs):
        cursor = self.conn.cursor()
        cmd = f"UPDATE {self.table_name} SET "
        items = [f"{key} = '{val}'" for key, val in kwargs.items()
                 if key != 'id']
        cmd += ", ".join(items)
        cmd += f" WHERE id = '{kwargs['id']}'"
        cursor.execute(cmd)
        self.conn.commit()
        cursor.close()