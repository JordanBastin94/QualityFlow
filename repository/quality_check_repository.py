
def create_quality_check(conn, quality_point_id, measured_value, status):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO quality_checks (
                quality_point_id,
                measured_value,
                status
            )
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (quality_point_id, measured_value, status),
        )
        return cursor.fetchone()[0]



def get_quality_points(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                qp.id,
                p.name,
                qp.name,
                qp.min_value,
                qp.max_value,
                qp.unit
            FROM quality_points qp
            JOIN products p ON p.id = qp.product_id
            ORDER BY qp.id
            """
        )
        return cursor.fetchall()
