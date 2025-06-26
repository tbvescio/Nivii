import pandas as pd
import psycopg2
from psycopg2 import sql
import os

DB_NAME = os.getenv('DB_NAME', 'nivii_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
CSV_FILE = os.getenv('CSV_FILE', 'data.csv')
TABLE_NAME = os.getenv('TABLE_NAME', 'sales_data')

print('Reading CSV...')
df = pd.read_csv(CSV_FILE)

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{TABLE_NAME}'
            )
        """)
        exists = cur.fetchone()[0]
        if exists:
            print(f"Table '{TABLE_NAME}' already exists. Exiting script.")
            return False
        cur.execute(f'''
            CREATE TABLE {TABLE_NAME} (
                date DATE,
                week_day VARCHAR(20),
                hour INTEGER,
                ticket_number VARCHAR(100),
                waiter VARCHAR(100),
                product_name VARCHAR(100),
                quantity INTEGER,
                unitary_price NUMERIC,
                total NUMERIC
            )
        ''')
        conn.commit()
        return True

def insert_data(conn, df):
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute(
                sql.SQL(f"""
                    INSERT INTO {TABLE_NAME} (
                        date, week_day, hour, ticket_number, waiter, product_name, quantity, unitary_price, total
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """),
                (
                    row['date'],
                    row['week_day'],
                    int(row['hour'].replace(":", "")),
                    row['ticket_number'],
                    row['waiter'],
                    row['product_name'],
                    int(row['quantity']),
                    float(row['unitary_price']),
                    float(row['total'])
                )
            )
        conn.commit()

if __name__ == '__main__':
    print('Connecting to database...')
    conn = get_connection()
    print('Creating table if not exists...')
    created = create_table(conn)
    if not created:
        conn.close()
        exit(0)
    print('Inserting data...')
    insert_data(conn, df)
    conn.close()
    print('Done!') 