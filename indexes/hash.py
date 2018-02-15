import time
from random import randint


def main():
    obj = HashMap()

    # Generate data
    n = 1000
    maxint = 200
    nums_k_v = [(randint(1, maxint), i) for i in range(n)]

    # Build hashMap
    obj.build(nums_k_v)

    # Get time for Hash
    time1 = time.time()

    for i in range(1, 10000):
        obj.search(20)

    print('Index search: ', time.time() - time1)

    # Check insertion
    obj.insert((101023012301203, "Hello!"))
    obj.insert((101023012301203, "Hola!"))
    obj.insert((101023012301203, "Hi!"))

    print(obj.search(101023012301203))

    # Check deletion
    obj.delete((101023012301203, "Hello!"))
    print(obj.search(101023012301203))

    # Get time for simple search
    time1 = time.time()
    returnList = []
    for i in range(1, 10000):
        for pair in nums_k_v:
            if "20".__eq__(pair[0]):
                returnList.append(pair)
    print('Simple search: ', time.time() - time1)


class HashMap:
    def __init__(self):
        self.num_of_buckets = 100
        self.buckets = [[] for _ in range(self.num_of_buckets)]

    # Takes List of Pairs (key, value)
    def build(self, list):
        for element in list:
            self.insert(element)

    # hashFunction
    def __hashFunction(self, key):
        return hash(key) % self.num_of_buckets

    # Insertion
    def insert(self, object):
        self.buckets[self.__hashFunction(object[0])].append(object)

    # Deletion
    def delete(self, object):
        self.buckets[self.__hashFunction(object[0])].remove(object)

    # Search
    def search(self, key):
        return_list = []
        for h in self.buckets[self.__hashFunction(key)]:
            if key is (h[0]):
                return_list.append(h)
        return return_list


if __name__ == '__main__':
    main()