from datetime import datetime, timedelta

class Plant:
    def __init__(self, name, water, sunlight):
        self.name = name
        self.water = int(water)        # hours
        self.sunlight = int(sunlight)  # hours

        self.last_watered = datetime.now()
        self.last_rotated = datetime.now()

    def next_water_date(self):
        return self.last_watered + timedelta(hours=self.water)

    def next_rotate_date(self):
        return self.last_rotated + timedelta(hours=self.sunlight)
