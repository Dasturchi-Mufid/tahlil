import datetime,calendar

def get_date(month: datetime.date):
    # Ensure month is a datetime.date object
    if isinstance(month, str):
        # If month is a string, convert it to a datetime.date object
        month = datetime.datetime.strptime(month, "%Y-%m").date()

    # First day of the month
    first_day = month.replace(day=1)

    # Correct calculation for the next month
    # If month is December (12), the next month should be January of the next year
    if month.month == 12:
        next_month = datetime.date(month.year + 1, 1, 1)
    else:
        next_month = month.replace(month=month.month + 1, day=1)

    # Subtract one day from the first day of the next month to get the last day of the current month
    last_day = next_month - datetime.timedelta(days=1)

    return first_day, last_day

def get_data(query,db,params=[]):
    
    db.execute(query,params)
    data = db.fetchall()
    return data
