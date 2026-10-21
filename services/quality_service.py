def determine_status(measured_value, min_value, max_value):
    if min_value <= measured_value <= max_value:
        return "pass"
    return "fail"