
def create_quality_alert(conn, quality_check_id, description, priority):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO quality_alerts (
                quality_check_id,
                description,
                priority
            )
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (quality_check_id, description, priority),
        )
        return cursor.fetchone()[0]
