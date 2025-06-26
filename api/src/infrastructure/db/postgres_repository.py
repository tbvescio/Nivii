import os
import psycopg2
from .repository import DatabaseRepository

class PostgresRepository(DatabaseRepository):
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'nivii_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres'),
            host=os.getenv('DB_HOST', 'db'),
            port=os.getenv('DB_PORT', '5432')
        )

    def execute(self, query: str):
        with self.conn.cursor() as cur:
            try:
                cur.execute(query)
                try:
                    result = cur.fetchall()
                except psycopg2.ProgrammingError:
                    result = None
                self.conn.commit()
                return result
            except Exception as e:
                self.conn.rollback()
                raise e

    def get_schema(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position
            """)
            rows = cur.fetchall()
            schema = {}
            for table, column, dtype in rows:
                if table not in schema:
                    schema[table] = []
                schema[table].append({'name': column, 'type': dtype})
            return schema 
