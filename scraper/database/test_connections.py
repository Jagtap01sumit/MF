from database.connections import engine
from sqlalchemy import text


class DatabaseConnection:

    @staticmethod
    def check_connection():
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("DB Connected Successfully:",result.fetchone())
        except Exception as e:
            print("DB Connection Failed:",e)