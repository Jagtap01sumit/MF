from sqlalchemy import text

from database.connections import engine


class TableCreation:
    @staticmethod
    def create_tables():

        queries = [
            # ======================================================
            # AMCS TABLE
            # ======================================================
            """
        CREATE TABLE IF NOT EXISTS amcs (

            id SERIAL PRIMARY KEY,

            amc_name VARCHAR(255)
            UNIQUE
            NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        );
        """,
            # ======================================================
            # SCHEMES TABLE
            # ======================================================
            """
        CREATE TABLE IF NOT EXISTS schemes (

            id SERIAL PRIMARY KEY,

            amc_id INTEGER
            REFERENCES amcs(id),

            scheme_code VARCHAR(100)
            UNIQUE
            NOT NULL,

            scheme_name TEXT,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        );
        """,
            # ======================================================
            # INDUSTRIES TABLE
            # ======================================================
            """
        CREATE TABLE IF NOT EXISTS industries (

            id SERIAL PRIMARY KEY,

            industry_name VARCHAR(255)
            UNIQUE
            NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        );
        """,
            # ======================================================
            # STOCKS TABLE
            # ======================================================
            """
        CREATE TABLE IF NOT EXISTS stocks (

            id SERIAL PRIMARY KEY,

            isin VARCHAR(50)
            UNIQUE
            NOT NULL,

            stock_name TEXT
            NOT NULL,

            industry_id INTEGER
            REFERENCES industries(id),

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        );
        """,
            # ======================================================
            # PORTFOLIO TABLE
            # ======================================================
            """
        CREATE TABLE IF NOT EXISTS portfolio (

            id SERIAL PRIMARY KEY,

            scheme_id INTEGER
            REFERENCES schemes(id),

            stock_id INTEGER
            REFERENCES stocks(id),

            report_month DATE
            NOT NULL,

            quantity BIGINT,

            market_value NUMERIC(20,2),

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(
                scheme_id,
                stock_id,
                report_month
            )
        );
        """,
        ]

        with engine.begin() as conn:
            for query in queries:
                conn.execute(text(query))

        print("✅ All tables created successfully")
