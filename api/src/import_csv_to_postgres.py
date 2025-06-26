import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date
from models import SalesData, Base

# Database connection parameters
DB_NAME = 'nivii_db'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'

CSV_FILE = 'data.csv'
TABLE_NAME = 'sales_data'

# Read CSV
print('Reading CSV...')
df = pd.read_csv(CSV_FILE)

# Connect to PostgreSQL
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
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
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

# Insert data into table
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
    create_table(conn)
    print('Inserting data...')
    insert_data(conn, df)
    conn.close()
    print('Done!') 