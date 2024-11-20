class Color:
    Reset = '\033[0m'
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'


class Errors:
    def __init__(self):
        pass

    @staticmethod
    def empty_data():
        return f"{Color.Red}Error: Cannot search for empty data in the tree!{Color.Reset}"

    @staticmethod
    def not_search(data):
        return f"{Color.Red}Error: Data not found in the tree! Data: {data} is not in the tree!{Color.Reset}"

    @staticmethod
    def equals_elements(data):
        return f"{Color.Red}Error: Duplicate element detected! Data: {data} cannot be added to the tree!{Color.Reset}"
