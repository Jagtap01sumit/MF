from sqlalchemy import text

from database.connections import engine

# ==========================================================
# GET OR CREATE AMC
# ==========================================================


def get_or_create_amc(amc_name):

    query = text("""

        INSERT INTO amcs(amc_name)

        VALUES (:amc_name)

        ON CONFLICT(amc_name)

        DO NOTHING;

    """)

    with engine.begin() as conn:

        conn.execute(query, {"amc_name": amc_name})

        result = conn.execute(
            text("""

                SELECT id

                FROM amcs

                WHERE amc_name = :amc_name

            """),
            {"amc_name": amc_name},
        ).fetchone()

    return result[0]


# ==========================================================
# GET OR CREATE SCHEME
# ==========================================================


def get_or_create_scheme(amc_id, scheme_code, scheme_name=None,fund_type=None):

    query = text("""

        INSERT INTO schemes(

            amc_id,
            scheme_code,
            scheme_name,
            fund_type

        )

        VALUES (

            :amc_id,
            :scheme_code,
            :scheme_name,
            :fund_type
        )

        ON CONFLICT(scheme_code)

        DO NOTHING;

    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {"amc_id": amc_id, "scheme_code": scheme_code, "scheme_name": scheme_name,"fund_type":fund_type},
        )

        result = conn.execute(
            text("""

                SELECT id

                FROM schemes

                WHERE scheme_code = :scheme_code

            """),
            {"scheme_code": scheme_code},
        ).fetchone()

    return result[0]


# ==========================================================
# GET OR CREATE INDUSTRY
# ==========================================================


def get_or_create_industry(industry_name):

    query = text("""

        INSERT INTO industries(
            industry_name
        )

        VALUES (
            :industry_name
        )

        ON CONFLICT(industry_name)

        DO NOTHING;

    """)

    with engine.begin() as conn:

        conn.execute(query, {"industry_name": industry_name})

        result = conn.execute(
            text("""

                SELECT id

                FROM industries

                WHERE industry_name = :industry_name

            """),
            {"industry_name": industry_name},
        ).fetchone()

    return result[0]


# ==========================================================
# GET OR CREATE STOCK
# ==========================================================


def get_or_create_stock(isin, stock_name, industry_id):

    query = text("""

        INSERT INTO stocks(

            isin,
            stock_name,
            industry_id
        )

        VALUES (

            :isin,
            :stock_name,
            :industry_id
        )

        ON CONFLICT(isin)

        DO NOTHING;

    """)

    with engine.begin() as conn:

        conn.execute(
            query, {"isin": isin, "stock_name": stock_name, "industry_id": industry_id}
        )

        result = conn.execute(
            text("""

                SELECT id

                FROM stocks

                WHERE isin = :isin

            """),
            {"isin": isin},
        ).fetchone()

    return result[0]


# ==========================================================
# INSERT PORTFOLIO ROW
# ==========================================================


def insert_portfolio(scheme_id, stock_id, report_month, quantity, market_value):

    query = text("""

        INSERT INTO portfolio(

            scheme_id,
            stock_id,
            report_month,
            quantity,
            market_value
        )

        VALUES (

            :scheme_id,
            :stock_id,
            :report_month,
            :quantity,
            :market_value
        )

        ON CONFLICT(

            scheme_id,
            stock_id,
            report_month

        )

        DO UPDATE SET

            quantity = EXCLUDED.quantity,

            market_value = EXCLUDED.market_value;

    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "scheme_id": scheme_id,
                "stock_id": stock_id,
                "report_month": report_month,
                "quantity": quantity,
                "market_value": market_value,
            },
        )

    print("✅ Portfolio row inserted")
