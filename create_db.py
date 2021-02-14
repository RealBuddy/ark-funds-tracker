import config
import csv
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""
    CREATE TABLE stock (
        id SERIAL PRIMARY KEY,
        symbol TEXT NOT NULL,
        name TEXT NOT NULL,
        exchange TEXT NOT NULL,
        is_etf BOOLEAN NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE etf_holding (
        etf_id INTEGER NOT NULL, 
        holding_id INTEGER NOT NULL,
        dt DATE NOT NULL, 
        shares NUMERIC,
        weight NUMERIC, 
        PRIMARY KEY (etf_id, holding_id, dt),
        CONSTRAINT fk_etf FOREIGN KEY (etf_id) REFERENCES stock (id),
        CONSTRAINT fk_holding FOREIGN KEY (holding_id) REFERENCES stock (id)
    );
""")

cursor.execute("""
    CREATE TABLE stock_price (
        stock_id INTEGER NOT NULL,
        dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        open NUMERIC NOT NULL, 
        high NUMERIC NOT NULL,
        low NUMERIC NOT NULL,
        close NUMERIC NOT NULL, 
        volume NUMERIC NOT NULL,
        PRIMARY KEY (stock_id, dt),
        CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
    );
""")

cursor.execute("""
    CREATE INDEX ON stock_price (stock_id, dt DESC);
""")

cursor.execute("""
    SELECT create_hypertable('stock_price', 'dt');
""")


connection.commit()