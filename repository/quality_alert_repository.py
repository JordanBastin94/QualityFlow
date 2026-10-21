
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


def get_all_quality_alerts(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT
                qa.id,
                p.name,
                qp.name,
                qc.measured_value,
                qp.unit,
                qa.description,
                qa.priority,
                qa.status,
                qa.corrective_action
            FROM quality_alerts qa
            JOIN quality_checks qc
                ON qc.id = qa.quality_check_id
            JOIN quality_points qp
                ON qp.id = qc.quality_point_id
            JOIN products p
                ON p.id = qp.product_id
            ORDER BY qa.id
        """)
        return cursor.fetchall()



def update_alert_status(conn, alert_id, new_status):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE quality_alerts
            SET status = %s
            WHERE id = %s
            RETURNING id
            """,
            (new_status, alert_id),
        )
        return cursor.fetchone()
