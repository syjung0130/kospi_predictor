import datetime

class TimeUtillHelper:
    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        self.time = datetime.datetime(year, month, day, hour, minute, second)

    def set_time(self, year, month, day, hour=0, minute=0, second=0):
        self.time = datetime.datetime(year, month, day, hour, minute, second)

    def __eq__(self, other_time):
        if(self.time == other_time.time):
            return True
        else:
            return False
    
    def __lt__(self, other_time):
        if(self.time < other_time.time):
            return True
        else:
            return False
    
    def __gt__(self, other_time):
        if(self.time > other_time.time):
            return True
        else:
            return False
    
    def __add__(self, other_time):
        return self.time + other_time.time

    def __str__(self):
        return self.time

    def get_datetime(self):
        return self.time

    def get_time_str(self):
        return self.time.strftime('%Y%m%d%H%M%S')

    def get_minute(self):
        return self.time.minute
    
    def get_hour(self):
        return self.time.hour

    def get_day(self):
        return self.time.day
    
    def get_month(self):
        return self.time.month

    def get_year(self):
        return self.time.year

    def get_weekday(self):
        return self.time.weekday()

    # class datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    def add_days(self, day_offset):
        days = datetime.timedelta(days=day_offset)
        self.time = self.time + days

    def add_hours(self, hour_offset):
        hours = datetime.timedelta(hours=hour_offset)
        self.time = self.time + hours

    def add_minutes(self, min_offset):
        minutes = datetime.timedelta(minutes=min_offset)
        self.time = self.time + minutes
    
    def add_seconds(self, second_offset):
        seconds = datetime.timedelta(seconds=second_offset)
        self.time = self.time + seconds



