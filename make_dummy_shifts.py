import random
from datetime import datetime, timedelta


# Function to generate a random datetime within the last 2 months
def random_date():
    end = datetime.now()
    start = end - timedelta(days=60)
    return start + (end - start) * random.random()


# Function to generate a random break duration
def random_break():
    return timedelta(minutes=random.randint(15, 60))


# List of user IDs
user_ids = [1, 2, 3]

# Number of dummy shifts to generate
num_dummy_shifts = 50

# Generate SQL statements
sql_statements = []

for _ in range(num_dummy_shifts):
    user_id = random.choice(user_ids)
    start_datetime = random_date()
    end_datetime = start_datetime + timedelta(hours=random.randint(4, 12))
    break_start = start_datetime + timedelta(hours=random.randint(1, 3))
    break_duration = random_break()
    status = "finished working"  # Status is always "finished working"

    sql = f"""
    INSERT INTO shifts (user_id, date, start_time, end_time, current_break_start, total_break, status)
    VALUES ({user_id}, '{start_datetime.date()}', '{start_datetime}', '{end_datetime}', '{break_start}', '{break_duration}', '{status}');
    """
    sql_statements.append(sql)

# Print out the SQL statements
for statement in sql_statements:
    print(statement)
