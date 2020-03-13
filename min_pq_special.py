"""Special Minimum Priority Queue
For:
    CPE202
    Sections 3 & 5
    Winter 2020
Author:
    Toshi
"""
class MinPQ:
    """Special Minimum Priority Queue
    Attributes:
        capacity (int): the capacity of the queue. The default capacity is 16.
        num_items (int): the number of items in the queue.
        arr (list): an array which contains the items in the queue.
    """
    def __init__(self, capacity=16, arr=None):
        if arr is None:
            self.capacity = capacity
            self.num_items = 0
            self.arr = [None] * self.capacity
            self.keys = [None] * (self.capacity + 1)
        else:
            self.arr = arr
            self.num_items = len(self.arr)
            self.capacity = self.num_items
            self.keys = [None] * (self.capacity + 1)
            self.heapify()

    def __eq__(self, other):
        return isinstance(other, MinPQ) and self.capacity == other.capacity\
            and self.num_items == other.num_items and self.arr == other.arr

    def __repr__(self):
        return "num_items=%d, arr=%s" % (self.num_items, self.arr)  

    def heapify(self):
        """initialize the queue with a given array and conver the array into a min heap
        """
        end = self.num_items - 1 
        idx = index_parent(end)
        while idx >= 0:
            self.keys[self.arr[idx].key] = idx 
            pos = self.shift_down(idx, end)
            idx -= 1

    def insert(self, item):
        """inserts an item to the queue
        Args:
            item (any): an item to be inserted to the queue. It is of any data type.
        Raises:
            IndexError : Raises IndexError when the queue is full 
        """
        if self.is_full():
            raise IndexError()
        self.arr[self.num_items] = item
        self.keys[item.key] = self.num_items
        self.num_items += 1
        self.shift_up(self.num_items - 1)

    def contains(self, key):
        """checks if the key exists in the queue
        Args:
            key (int): a key
        Returns:
            bool: True if exists False otherwise
        """
        return key <= self.capacity + 1 and self.keys[key] is not None

    def change_key(self, key):
        """change the priority of the item with the key
        Args:
            key (int): a key
        Raises:
            KeyError: if the key does not exist
        """
        if not self.contains(key):
            raise KeyError()
        i = self.keys[key]
        self.shift_up(i)

    def del_min(self):
        """deletes the minimum item in the queue
        Returns:
            any : it returns the minimum item, which has just been deleted
        Raises:
            IndexError : Raises IndexError when the queue is empty
        """
        if self.is_empty():
            raise IndexError()
        item = self.arr[0]
        self.keys[item.key] = None
        self.num_items -= 1
        self.arr[0] = self.arr[self.num_items]
        k = self.arr[0].key
        self.keys[k] = 0
        self.shift_down(0, self.num_items - 1)
        return item

    def min(self):
        """returns the minimum item in the queue without deleting the item
        Returns:
            any : it returns the minimum item 
        Raises:
            IndexError : Raises IndexError when the queue is empty
        """
        if self.is_empty():
            raise IndexError()
        return self.arr[0] 

    def is_empty(self):
        """checks if the queue is empty 
        Returns:
            bool : True if empty, False otherwise. 
        """
        return self.num_items == 0 

    def is_full(self):
        """checks if the queue is full 
        Returns:
            bool : True if empty, False otherwise. 
        """
        return self.num_items == self.capacity 

    def size(self):
        """returns the number of items in the queue 
        Returns:
            int : it returns the number of items in the queue 
        """
        return self.num_items 

    def shift_up(self, idx):
        """shifts up an item at idx
        Args:
            idx (int): the index of an item
        """
        pidx = index_parent(idx)
        while idx > 0 and self.arr[idx] < self.arr[pidx]:
            self.arr[idx], self.arr[pidx] = self.arr[pidx], self.arr[idx]
            k1 = self.arr[idx].key
            self.keys[k1] = idx
            k2 = self.arr[pidx].key
            self.keys[k2] = pidx 
            idx = pidx
            pidx = index_parent(idx)

    def shift_down(self, idx, end):
        """shifts down an item at idx
        Args:
            idx (int): the index of an item
            end (int): the index of the last item
        """
        while idx < end:
            left = index_left(idx)
            right = index_right(idx)
            imin = index_smaller(self.arr, left, right, end)
            if imin > end or self.arr[idx] < self.arr[imin]:
                return 
            self.arr[idx], self.arr[imin] = self.arr[imin], self.arr[idx]
            k1 = self.arr[idx].key
            self.keys[k1] = idx
            k2 = self.arr[imin].key
            self.keys[k2] = imin
            idx = imin
        return

def index_parent(idx):
    """compute the index of parent
    Args:
        idx (int): the index of the item
    Returns:
        int: the index
    """
    return (idx - 1) // 2

def index_left(idx):
    """compute the index of left child 
    Args:
        idx (int): the index of the item
    Returns:
        int: the index
    """
    return idx * 2 + 1

def index_right(idx):
    """compute the index of right child 
    Args:
        idx (int): the index of the item
    Returns:
        int: the index
    """
    return idx * 2 + 2

def index_smaller(arr, left, right, end):
    """compute the index of the smaller child 
    Args:
        arr (list): the array
        left (int): the index of left child 
        right (int): the index of right child
        end (int): the index of the end
    Returns:
        int: the index
    """
    if left > end or right > end:
        return left
    if arr[left] < arr[right]:
        return left
    return right
