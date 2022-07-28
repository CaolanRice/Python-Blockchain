class Car:
    # top_speed = 120
    # __warnings = []
    def __init__(self, starting_speed=100):
        #instance attributes
        self.top_speed = starting_speed
        self.__warnings = []
    def __repr__(self):
        print('Printing')
        return 'Top speed: {}, Warnings: {}'.format(self.top_speed, len(self.__warnings))
    
    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings


    def drive(self):
        print('I am driving but certainly not faster than {}'.format(self.top_speed))

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