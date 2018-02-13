class A:

    def __init__(self, val: int) -> None:
        self.value = val

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __str__(self):
        return str(self.value)

a = [1,2,3,3,3, 5, 9]
b = list(map(A, a))

from bisect import bisect_right

c = 10
print(b)
print(bisect_right(a, c))
print(bisect_right(b, A(c)))

    