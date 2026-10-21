from database.db import get_connection

def main():
    try:
        with get_connection() as connection:
            print("Connection successful!")

    except Exception as error:
        print(f"Connection failed: {error}")


if __name__ == "__main__":
    main()
