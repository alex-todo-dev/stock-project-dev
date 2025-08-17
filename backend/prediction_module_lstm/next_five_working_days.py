from datetime import datetime, timedelta
import holidays

def next_five_working_days(start_date_str, country='US'):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    holiday_set = holidays.country_holidays(country)
    working_days = []
    current_date = start_date + timedelta(days=1)

    while len(working_days) < 5:
        if current_date.weekday() < 5 and current_date not in holiday_set:
            working_days.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return working_days

# Example usage
# input_date = "2025-06-22"
# print(next_five_working_days(input_date, country='US'))  # Replace 'US' with your country code if needed
