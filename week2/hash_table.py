
# %%
from ctypes import resize
import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value


# draft
# def char_num(char):
#     char_to_num = {"a": 2, "b": 3, "c": 5, "d": 7, "e": 11, "f": 13, "g": 17, "h": 19, "i": 23, "j": 29, "k": 31, "l": 37, "m": 41, "n": 43, "o": 47, "p": 53, "q": 59, "r": 61, "s": 67, "t": 71, "u": 73, "v": 79, "w": 83, "x": 89, "y": 97, "z": 101,}
    
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    hash = 1
    for i in key:
        hash *= ord(i)
    return hash


# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        self.resize()
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        prev_item = None
        while item:
            if item.key == key:
                if item == self.buckets[bucket_index]:
                    self.buckets[bucket_index] = item.next
                else:
                    prev_item.next = item.next
                self.item_count -= 1
                self.resize()
                return True
            else:
                prev_item = item
            item = item.next
        return False
    
    

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)
        
    def is_resize_double(self):
        if self.bucket_size * 0.7 < self.item_count:
            return True
        return False
    
    def is_resize_half(self):
        # 要素数がテーブルサイズの　30% を下回った場合
        if self.bucket_size * 0.3 > self.item_count:
            return True
        return False
    
    # 奇数になるよう調整
    def to_odd(self,num):
        if num % 2 == 0:
            num += 1
        return num
    
    # ヒント 2🤗
    # 再ハッシュを実装してデータを追加してもほぼ O(1) で動くようにしよう
    # 作り方の例：
    # 要素数がテーブルサイズの 70% を上回ったら、テーブルサイズを 2 倍に拡張
    # 要素数がテーブルサイズの 30% を下回ったら、テーブルサイズを半分に縮小
    # テーブルサイズは奇数（できれば素数）になるよう調整するとハッシュの衝突が減ります

    def rehash(self):
        old_hash = self.buckets
        self.buckets = [None] * self.bucket_size
        for item in old_hash:
            while item:
                next_item = item.next
                new_index = calculate_hash(item.key) % self.bucket_size
                item.next = self.buckets[new_index]
                self.buckets[new_index] = item
                item = next_item

    

    def resize(self):
        if self.is_resize_double():
            self.bucket_size *= 2
            self.bucket_size = self.to_odd(self.bucket_size)
            self.rehash()
        elif self.is_resize_half():
            self.bucket_size //= 2
            self.bucket_size = self.to_odd(self.bucket_size)
            self.rehash()



# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))
    
    

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":

    start = time.perf_counter()
    #functional_test()
    performance_test()
    end = time.perf_counter()
    excution_time = end - start
    print(f"Execution time : {excution_time} seconds")

# %%

# visualize
from matplotlib import pyplot as plt
x = [10000 * i for i in range(100)]
y1 = [
    0.086309, 0.141542, 0.202554, 0.262550, 0.350877, 0.413893, 0.495266, 0.651208,
    0.982938, 1.093976, 1.424547, 1.680312, 2.053131, 2.401938, 2.820783, 3.243775,
    3.865148, 4.017057, 4.383031, 4.894019, 5.245859, 5.618590, 6.034441, 6.463551,
    6.869392, 7.260364, 7.720317, 8.740745, 8.830340, 9.117516, 9.668195, 9.953004,
    12.332527, 11.231821, 11.384634, 11.707966, 12.922308, 12.254276, 12.730150, 13.072281,
    13.978588, 14.158214, 15.347943, 15.332875, 15.473192, 16.035329, 16.586896, 16.891870,
    17.337582, 17.843162, 18.444680, 18.517569, 18.670502, 19.165287, 19.991839, 19.568051,
    20.491242, 20.429838, 21.449067, 21.823369, 21.717038, 22.039282, 23.332333, 23.552110,
    34.545949, 24.076877, 25.166477, 24.930728, 25.212562, 25.674818, 25.995456, 27.264397,
    26.537497, 27.503351, 28.288542, 27.751970, 28.678446, 28.949422, 28.911345, 29.713363,
    29.687544, 30.610669, 30.928979, 31.282778, 31.299691, 33.144411, 32.320645, 32.349620,
    32.819852, 33.936807, 34.204497, 34.494442, 34.421354, 34.379912, 36.208493, 36.397774,
    36.649880, 36.274377, 36.250461, 36.548504
]
y2 = [
    0.064673, 0.032741, 0.035836, 0.027418, 0.048097, 0.029373, 0.032031, 0.033566,
    0.099721, 0.048356, 0.055038, 0.213108, 0.069713, 0.072183, 0.077560, 0.087566,
    0.142481, 0.047914, 0.051453, 0.051247, 0.050239, 0.052898, 0.055258, 0.060470,
    0.056710, 0.057513, 0.061857, 0.312189, 0.068137, 0.067484, 0.069522, 0.072294,
    0.273009, 0.072267, 0.076174, 0.075707, 0.080322, 0.081342, 0.082420, 0.084605,
    0.084658, 0.086385, 0.089036, 0.090729, 0.095021, 0.096955, 0.096790, 0.099074,
    0.505506, 0.101779, 0.101477, 0.105981, 0.106592, 0.107685, 0.112461, 0.111742,
    0.115785, 0.115036, 0.117010, 0.122660, 0.121221, 0.126231, 0.123723, 0.130392,
    0.533390, 0.138632, 0.134885, 0.138420, 0.137723, 0.137893, 0.141316, 0.144269,
    0.147296, 0.754324, 0.147595, 0.176316, 0.149889, 0.153016, 0.152634, 0.156170,
    0.155254, 0.158728, 0.160544, 0.163292, 0.162336, 0.168812, 0.167030, 0.168241,
    0.165179, 0.177061, 0.174070, 0.175896, 0.177582, 0.179967, 0.180343, 0.183187,
    0.185708, 0.185584, 0.186862, 0.191735
]
plt.scatter(x, y1, marker='o', label = "hash : sum")
plt.scatter(x, y2, marker='o', label = "hash : product")
plt.xlabel("Items")
plt.ylabel("Executed time (seconds)")
plt.title("Relationship between Hash Functions and Execution Time")
plt.legend()
plt.grid(True)
plt.show()
# %%
