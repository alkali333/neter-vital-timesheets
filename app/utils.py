from datetime import timedelta, datetime


def format_timedelta(td):
    if not td:
        return "None"
    total_minutes = td.total_seconds() // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{int(hours)} hours {int(minutes)} minutes"


# Example usage:
td = timedelta(hours=2, minutes=10, seconds=57, microseconds=433451)
formatted = format_timedelta(td)
print(formatted)
