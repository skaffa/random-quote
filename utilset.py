import time

def get_seconds(years=0, months=0, weeks=0, days=0, hours=0, minutes=0, milliseconds=0):
    seconds = 0
    # Convert years to days
    seconds += years * 365.25 * 24 * 60 * 60
    # Convert months to days (assuming 30 days per month)
    seconds += months * 30 * 24 * 60 * 60
    # Convert weeks to days
    seconds += weeks * 7 * 24 * 60 * 60
    # Convert days to seconds
    seconds += days * 24 * 60 * 60
    # Convert hours to seconds
    seconds += hours * 60 * 60
    # Convert minutes to seconds
    seconds += minutes * 60
    # Convert milliseconds to seconds
    seconds += milliseconds / 1000
    
    return int(seconds)