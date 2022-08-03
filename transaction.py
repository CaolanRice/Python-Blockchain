from collections import OrderedDict
from printable import Printable

#inheriting Printable class
class Transaction(Printable):

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('receiver', self.reciever), ('amount', self.amount)])

    def __init__(self, sender, receiver, amount):
        self.sender = sender,
        self.reciever = receiver,
        self.amount = amount


