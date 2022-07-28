class Bus:
    # top_speed = 120
    # __warnings = []
    def __init__(self, starting_speed=100):
        #instance attributes
        self.top_speed = starting_speed
        self.__warnings = []
        self.passengers = []
    def __repr__(self):
        print('Printing')
        return 'Top speed: {}, Warnings: {}'.format(self.top_speed, len(self.__warnings))
    
    def add_warning(self, warning_text):
        if len(warning_text) > 0:
            self.__warnings.append(warning_text)

    def get_warnings(self):
        return self.__warnings
    
    def brag(self):
        print('Look how cool my car is')


    def drive(self):
        print('I am driving but certainly not faster than {}'.format(self.top_speed))

    def add_group(self, passengers):
        self.passengers.extend(passengers)
