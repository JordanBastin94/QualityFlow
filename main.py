from repository.product_repository import get_all_products, create_product
from database.db import get_connection
import psycopg
from repository.quality_check_repository import get_quality_points,create_quality_check
from services.quality_service import determine_status
from repository.quality_alert_repository import create_quality_alert, get_all_quality_alerts, update_alert_status
from services.quality_service import build_alert_details

def main():
    while True:
        print("\n=== QualityFlow ===")
        print("1. List products")
        print("2. Add product")
        print("3. Record quality check")
        print("4. View quality alerts")
        print("5. Update quality alert status")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            with get_connection() as conn:
                products = get_all_products(conn)

            if not products:
                print("No products found.")
            else:
                for product in products:
                    print(product)

        elif choice == "2":
            reference = input("Product reference: ").strip()
            name = input("Product name: ").strip()
            description = input("Description (optional): ").strip() or None

            if not reference or not name:
                print("Reference and name are required.")
                continue

            try:
                with get_connection() as conn:
                    product_id = create_product(
                        conn, reference, name, description
                    )

                print(f"Product created successfully (ID: {product_id}).")

            except psycopg.errors.UniqueViolation:
                print("A product with this reference already exists.")

            except psycopg.Error as error:
                print(f"Database error: {error}")

        elif choice == "3":
            try:
                with get_connection() as conn:
                    quality_points = get_quality_points(conn)

                    if not quality_points:
                        print("No quality points available.")
                        continue

                    print("\nAvailable quality points:")

                    for point in quality_points:
                        point_id, product_name, point_name, min_value, max_value, unit = point
                        print(
                            f"{point_id}. {product_name} - {point_name} "
                            f"({min_value} to {max_value} {unit})"
                        )

                    try:
                        quality_point_id = int(input("Choose a quality point ID: "))
                    except ValueError:
                        print("Invalid ID.")
                        continue

                    selected_point = next(
                        (point for point in quality_points if point[0] == quality_point_id),
                        None,
                    )

                    if selected_point is None:
                        print("Quality point not found.")
                        continue

                    _, _, point_name, min_value, max_value, unit = selected_point

                    try:
                        measured_value = float(
                            input(f"Enter measured value ({unit}): ")
                        )
                    except ValueError:
                        print("Invalid measurement.")
                        continue

                    
                    status = determine_status(
                        measured_value,
                        min_value,
                        max_value,
                    )

                    check_id = create_quality_check(
                        conn,
                        quality_point_id,
                        measured_value,
                        status,
                    )

                    if status == "fail":
                        description, priority = build_alert_details(
                            point_name,
                            measured_value,
                            min_value,
                            max_value,
                            unit,
                        )

                        alert_id = create_quality_alert(
                            conn,
                            check_id,
                            description,
                            priority,
                        )

                        print(f"Quality alert created (ID: {alert_id}).")


                print(f"Quality check recorded (ID: {check_id}).")
                print(f"Result: {status.upper()}")

            except psycopg.Error as error:
                print(f"Database error: {error}")

        
        elif choice == "4":
            with get_connection() as conn:
                alerts = get_all_quality_alerts(conn)

            if not alerts:
                print("No quality alerts found.")
            else:
                for alert in alerts:
                    (
                        alert_id,
                        product_name,
                        point_name,
                        measured_value,
                        unit,
                        description,
                        priority,
                        status,
                        corrective_action,
                    ) = alert

                    print(f"\nAlert #{alert_id}")
                    print(f"Product: {product_name}")
                    print(f"Quality point: {point_name}")
                    print(f"Measured value: {measured_value} {unit}")
                    print(f"Description: {description}")
                    print(f"Priority: {priority.upper()}")
                    print(f"Status: {status}")
                    print(f"Corrective action: {corrective_action or 'Not defined'}")

        
        elif choice == "5":
            try:
                alert_id = int(input("Enter alert ID: "))
            except ValueError:
                print("Invalid alert ID.")
                continue

            print("1. open")
            print("2. in_progress")
            print("3. resolved")

            status_choice = input("Choose new status: ")

            statuses = {
                "1": "open",
                "2": "in_progress",
                "3": "resolved",
            }

            new_status = statuses.get(status_choice)

            if new_status is None:
                print("Invalid status.")
                continue

            try:
                with get_connection() as conn:
                    result = update_alert_status(conn, alert_id, new_status)

                if result is None:
                    print("Alert not found.")
                else:
                    print(f"Alert #{alert_id} updated to {new_status}.")

            except psycopg.Error as error:
                print(f"Database error: {error}")

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()