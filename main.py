import time

# generate a list L of items with len(L) = 20 000 # each item has a key() and data() methods 
list_size = 20000
a_long_list = get_long_list_of_items(list_size)
# a random item from the list (L.index(item) > len(L) / 2)
item = get_item_of_interest(a_long_list)
# a naive sequential search for baseline perfomance check 
def naive_search(l, item):
    for i, p in enumerate(l):
        if p.key() == item.key()
            return i
# measure naive time
start = time.time() 
naive_search(a_long_list, item) 
end = time.time()
t_no_idx = end - start
# build index on list
idx_set = build_index(a_long_list)
# measure index lookup time start = time.time() idx_set.look_up(item)
end = time.time()
t_idx = end - start
# make sure that indexed operation is faster
assert t_idx < t_no_idx, 'Your implementation sucks!'


index = MyIndex()
index.build_index()