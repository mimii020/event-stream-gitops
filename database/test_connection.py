from database.connection import get_connection

def main():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT current_database(), current_user"
        ).fetchone()

        print(f"Database: {result[0]}")
        print(f"User: {result[1]}")


if __name__ == "__main__":
    main()