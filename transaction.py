from collections import OrderedDict

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender,
        self.reciever = receiver,
        self.amount = amount

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('receiver', self.reciever), ('amount', self.amount)])
