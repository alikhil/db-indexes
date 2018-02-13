from typing import TypeVar, Generic, List
from bisect import bisect_right

T = TypeVar('T')

PAGE_SIZE = 4

class SmartKey(Generic[T]):

    def __init__(self, key: int, value: T = None) -> None:
        self.key = key
        self.value = value


    def __str__(self):
        return f"[{self.key}] => {self.value}"

# public class Page<Key>
#     Page(boolean bottom) 
#     void close()
#     void add(Key key)
#     void add(Page p)
#     boolean isExternal() 
#     boolean contains(Key key)
#     Page next(Key key) 
#     boolean isFull()
#     Page split() I
#     terable<Key> keys()

class KeyWrapper:

    def __init__(self, key: SmartKey, link: 'Page' = None) -> None:
        self.smart_key = key
        self.link = link

    def __lt__(self, other) -> bool:
        if isinstance(other, KeyWrapper):
            return self.smart_key.key < other.smart_key.key
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, KeyWrapper):
            return self.smart_key.key == other.smart_key.key
        return False
    # TODO: implment other operators?

    def print(self, tabs):
        if self.link:
            self.link.print_tree(len(tabs) + 1)
        else:
            return print(tabs, str(self.smart_key))

class Page:
    def __init__(self, bottom: bool) -> None:
        self.bottom = bottom
        self.elements: List[KeyWrapper] = []

    
    def close(self) -> None:
        pass

    def add_key(self, key: SmartKey) -> None:
        """put key into the (external) page"""

        wrapped_key = KeyWrapper(SmartKey(key.key, [key.value])) # storing list of values in bottom nodes

        if len(self.elements) == 0:
            self.elements.append(wrapped_key)
        else:
            left_upper_index = bisect_right(self.elements, wrapped_key)
            if (left_upper_index > 0 and self.elements[left_upper_index - 1].smart_key.key == wrapped_key.smart_key.key):
                self.elements[left_upper_index - 1].smart_key.value.append(key.value)
            else: 
                self.elements.insert(left_upper_index, wrapped_key)

    def add_page(self, page: 'Page') -> None:
        """
            open p and put an entry into this (internal) page that
            associates the smallest key in p with p
        """
        # assume that we don't have any kw in current page with same kw as in given page 
        head_key_w = page.elements[0]
        left_upper_index = bisect_right(self.elements, head_key_w)
        self.elements.insert(left_upper_index, KeyWrapper(head_key_w.smart_key, page))


    def is_external(self) -> bool:
        return self.bottom

    def find(self, key: SmartKey) -> SmartKey:
        """Try to find key in page"""
        wrapped_key = KeyWrapper(key)
        left_upper_index = bisect_right(self.elements, wrapped_key)

        if left_upper_index == 0: # or left_upper_index == len(self.elements)): # I forget why I put this
            return None
        
        prev = self.elements[left_upper_index - 1]
        if (prev.smart_key.key == key.key and not prev.link):
            return self.elements[left_upper_index - 1].smart_key
        else:
            if prev.link:
                print("find can not be executed in internal node!")
                return prev.link.find(key)
            else: 
                return None # there is page that could contain key but it has no link

    def next(self, key: SmartKey) -> 'Page':
        left_upper_index = bisect_right(self.elements, KeyWrapper(key))
        if left_upper_index == 0:
            print("next is going to return None. it should not happen!")
            return None
        else:
            return self.elements[left_upper_index - 1].link


    def is_full(self) -> bool:
        return len(self.elements) == PAGE_SIZE

    def split(self) -> 'Page':
        """
            move the highest-ranking half of the keys in the page to a new page
        """
        # should create with same bottom
        new_page_els = self.elements[PAGE_SIZE // 2:]     # last half
        self.elements = self.elements[:PAGE_SIZE // 2]    # first half

        new_page = Page(self.bottom)
        new_page.elements = new_page_els
        return new_page

    def keys(self) -> List[SmartKey]:
        return None

    def print_tree(self, deep = 0) -> None:

        if self.is_external():
            tabs = '\t' * deep
            for child in self.elements:
                child.print(tabs)
        # else:
            # self.



class BTree:

    def __init__(self, sentinel: SmartKey) -> None:
        """
            sentinel key should be less then any other keys
        """
        self.root = Page(True)
        self.add_key(sentinel)

    def add_key(self, key: SmartKey) -> None:
        self._put(self.root, key)
        if self.root.is_full():
            left = self.root
            right = self.root.split()
            
            self.root = Page(False)

            self.root.add_page(left)
            self.root.add_page(right)

    def find_key(self, key: SmartKey) -> SmartKey:
        return self._find(self.root, key)


    def _find(self, h: Page, key: SmartKey) -> SmartKey:
        if h is None:
            return None
        
        if h.is_external(): 
            return h.find(key)
        
        return self._find(h.next(key), key)

    def _put(self, page: Page, key: SmartKey) -> None:

        if page.is_external():
            page.add_key(key)
            return
        
        nxt = page.next(key)
        self._put(nxt, key)
        if nxt.is_full():
            page.add_page(nxt.split())
        
        nxt.close()
    
    def print_tree(self, deep: int = 0) -> None:
        self.root.print_tree(deep)
        


class NaiveTreeIndex:

    def __init__(self, *args, **kwargs) -> None:
        self.tree: dict = {}

    def add_key(self, key: SmartKey):
        if key.key in self.tree:
            self.tree[key.key].append(key.value)
        else:
            self.tree[key.key] = [key.value]

    def find(self, key: SmartKey) -> SmartKey:
        return SmartKey(key.key, self.tree[key.key]) if key.key in self.tree else None

class NaiveListIndex:

    def __init__(self, *args, **kwargs):
        self.list = []
    
    def add_key(self, key: SmartKey):
        for k, v in self.list:
            if k == key.key:
                v.append(key.value)
                return 
        self.list.append((key.key, [key.value]))


    def find_key(self, key:SmartKey):
        for k, v in self.list:
            if k == key.key:
                return self.list[k]

        return None
        

from random import shuffle, randint
import time

if __name__ == "__main__":
    # nums = [13, 8, 3, 2, 5, 1, 1]
    n = 10000
    maxint = 100
    
    nums_k_v = [(i, randint(1, maxint)) for i in range(n)]
    # cp = nums[:]
    # shuffle(nums)
    # print("nums order is folowing:", nums) 

    btree = BTree(SmartKey(-1))
    naive = NaiveTreeIndex()
    naiveL = NaiveListIndex()

    st = time.time()
    for k,v in nums_k_v:
        btree.add_key(SmartKey(k, v))

    et = time.time();
    print('btree build:', et - st)

    st = time.time()
    for k,v in nums_k_v:
        naive.add_key(SmartKey(k, v))
    et = time.time();
    print('naive build:', et - st)

    st = time.time()
    for k,v in nums_k_v:
        naiveL.add_key(SmartKey(k, v))
    et = time.time();
    print('naive list build:', et - st)



    cp = nums_k_v[:]
    shuffle(cp)

    st = time.time()
    for k, _ in cp:
        naive.find(SmartKey(k))

    et = time.time();


    print('naive:', et - st)


    st = time.time()
    for k, _ in cp:
        btree.find_key(SmartKey(k))


    et = time.time();

    print('btree:', et - st)

    st = time.time()
    for k, _ in cp:
        naiveL.find_key(SmartKey(k))


    et = time.time();

    print('naive list:', et - st)
    # cnt = 0
    # for k, _ in cp:
    #     s = btree.find_key(SmartKey(k))
    #     ns = naive.find(SmartKey(k))
    #     if not ns:
    #         print('naive failed')
    #         print(k)
    #         continue
    #     if not s:
    #         print('btree failed')
    #         print(k)
    #         continue
    #     if ns.value == s.value:
    #         print("ok")
    #     else:
    #         cnt += 1
    #         print(k, 'naive:', ns.value, 'btree:', s.value)
    # print(cnt)