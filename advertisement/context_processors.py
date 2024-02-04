from datetime import date, timedelta


def get_date_today(request):
    date_today = date.today()
    date_yesterday = date_today - timedelta(1)
    return {"date_today": date_today, "date_yesterday": date_yesterday}
