import vehicle
# from vehicle import Vehicle

class Car(vehicle.Vehicle):

    def brag(self):
        print('Look how cool my car is')

car1 = Car()
car1.drive()

# Car.top_speed = 200
car1.add_warning('New wasdas')
# car1.__warnings.append([])
# print(car1.__dict__)
print(car1)


car2 = Car(200)
car2.drive()
# car2.__warnings.append('Hehe')
print(car2)

car3 = Car(300)
car3.drive()
print(car3)