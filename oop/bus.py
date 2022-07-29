from vehicle import Vehicle

class Bus(Vehicle):

    def __init__(self, starting_speed=100):
        super().__init__(starting_speed)
        self.passengers = []

    #expect that passengers is a list, take all the list elements and add it to self.passengers
    def add_group(self, passengers):
        self.passengers.extend(passengers)

bus1 = Bus(200)
bus1.add_group(['Caolan', 'Anna'])
print(bus1.passengers)
bus1.drive()
