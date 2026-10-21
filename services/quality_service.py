def determine_status(measured_value, min_value, max_value):
    if min_value <= measured_value <= max_value:
        return "pass"
    return "fail"


def build_alert_details(quality_point_name, measured_value, min_value, max_value, unit):
    description = (
        f"{quality_point_name}: measured value {measured_value} {unit}, "
        f"expected between {min_value} and {max_value} {unit}."
    )
    priority = "high"

    return description, priority
