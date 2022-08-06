"""Enables printing of dictionaries as a String """

class Printable:
    def __repr__(self):
        return str(self.__dict__)  