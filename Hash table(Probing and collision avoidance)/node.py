class Node:
    def __init__(self, item, next):
        self.item = item
        self.next = next

    def __str__(self):
        return str(self.item)
