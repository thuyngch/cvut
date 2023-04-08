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
        # check if table exist or not
        cur = self.conn.cursor()
        cur.execute(
            "select * from information_schema.tables where table_name=%s", (self.table_name,))
        table_existed = bool(cur.rowcount)
        if not table_existed:
            raise RuntimeError(f"table {self.table_name} does not exist")

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

    def query_records(self, **kwargs):
        cursor = self.conn.cursor()
        conditions = []
        for key, val in kwargs.items():
            if isinstance(val, str):
                val = f"'{val}'"
            conditions.append(f"{key}={val}")
        conditions = " AND ".join(conditions)
        cmd = f"SELECT * FROM {self.table_name} WHERE {conditions} ORDER BY time"
        cursor.execute(cmd)
        records = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        return records, colnames

    def remove_all_records(self, ):
        cursor = self.conn.cursor()
        cmd = f"TRUNCATE {self.table_name}"
        cursor.execute(cmd)
        self.conn.commit()
        cursor.close()

    def remove_one_record(self, id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE id = '{id}'")
        self.conn.commit()
        cur.close()
