from db.connections import engine
from sqlalchemy import text

def connectionEstablistion():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ DB Connected Successfully:", result.fetchone())

    except Exception as e:
        print("❌ DB Connection Failed:", e)
