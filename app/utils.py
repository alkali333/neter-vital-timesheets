from datetime import timedelta, datetime


def format_timedelta(td):
    if not td:
        return "None"
    total_minutes = td.total_seconds() // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{int(hours)} hours {int(minutes)} minutes"


def calculate_hours_worked(start_time):
    # Get the current time
    current_time = datetime.now()

    # Calculate the time delta between now and the start time
    time_worked = current_time - start_time

    return time_worked


# Example usage:
td = timedelta(hours=2, minutes=10, seconds=57, microseconds=433451)
formatted = format_timedelta(td)
print(formatted)
