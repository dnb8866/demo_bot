from datetime import date


async def validate_dates(input_text, month, year):
    if not input_text or not isinstance(input_text, str):
        return False
    dates_of_month = list(map(lambda x: x.strip(), input_text.strip().split(',')))
    for date_of_month in dates_of_month:
        try:
            date(year, month, int(date_of_month))
        except ValueError:
            return False
    return True



