from psycopg import Connection


def get_all_products(conn: Connection):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, reference, name, description
            FROM products
            ORDER BY id
        """)
        return cursor.fetchall()

def create_product(conn, reference, name, description):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO products (reference, name, description)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (reference, name, description),
        )
        return cursor.fetchone()[0]