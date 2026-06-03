from database.connections import engine

def insert_holdings(df):
    try:
        df.to_sql(
            name="mf_holdings",
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

        print("✅ Data inserted into mf_holdings successfully")

    except Exception as e:
        print(f"❌ DB Insert Failed: {e}")
        raise