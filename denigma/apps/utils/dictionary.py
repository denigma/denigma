"""Search a dictionary for key or value using named functions or a class."""


def find_key(div, val):
    """"Returns the key of dictionary dic given the value."""
    return [k for k, v in symbol_dic.iteritems() if v == val][0]

def find_value(dic, key):
    """Returns the value of dictionary dic given the key."""
    return dic[key]


class Lookup(dict):
    """A dictionary which can lookup value by key, or keys by value."""
    def __init__(self, items=[]):
        """Items can be a list of pair_lists or a dictionary."""
        dict.__init__(self, items)

    def get_key(self, value):
        """Find the key(s) as a list given a value."""
        return [item[0] for item in self.items() if item[1] == value]

    def get_value(self, key):
        """Find the value given a key."""

# Test it out:
if __name__ == '__main__':

    # Dictionary of chemical symbols:
    symbol_dic = {
        'C': 'carbon',
        'H': 'hydrogen',
        'N': 'nitrogen',
        'Li': 'lithium',
        'Be': 'berilium',
        'B': 'boron'
    }

    print(find_key(symbol_dic, 'boron'))    # B
    print(find_value(symbol_dic, 'B'))      # boron
    print(find_value(symbol_dic, 'H'))      # hydrogen

    name = 'lithium'
    symbol = 'Li'
    # Use a dictionary:
    look = Lookup(symbol_dic)
    print(look.get_key(name))    # ['Li']
    print(look.get_value(symbol))# lithium

    # Use a list of pairs instead of a dictionary.