class Plant:
    name = "null"
    water = "null"
    sunlight = "null"

    def __init__(self, name, water, sunlight):
        self.name = name
        self.water = water
        self.sunlight = sunlight
        
    def display_info(self):
        return f"This plant is a {self.name} , water: {self.water} , sunlight: {self.sunlight}."