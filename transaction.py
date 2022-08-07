from collections import OrderedDict
from inspect import signature
from utility.printable_dict import Printable

#inheriting Printable class
class Transaction(Printable):
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.signature = signature
        self.amount = amount

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])




