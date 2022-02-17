from .models import Day

def GetDate(request):
    days = Day.objects.last()
    return {"days":days}

def get_latest_day_number(request):
    day = Day.objects.last()
    if day:
        day_number = day.number
    else:
        day_number = 1
    return {"day_number": 1}