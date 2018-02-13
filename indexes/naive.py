"""
Index by using list
"""
from abstract import AbstractIndex

class NaiveIndex(AbstractIndex):

    def __init__(self):
        self.list = []

    def add(self, elem):
        self.list.append(elem)

    def remove(self, elem):
        self.list.remove(elem)

    @classmethod
    def find(self, elem):
        # for elem in self.list:
        pass
        # return self.list.