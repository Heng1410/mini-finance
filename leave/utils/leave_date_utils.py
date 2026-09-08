from datetime import date


def calculate_leave_days(start_date: date, end_date: date) -> int:
    if end_date < start_date:
        raise ValueError(
            "End date must be greater than or equal to start date."
        )
    return (end_date - start_date).days + 1