# %%
import sys
import time
from hash_table import HashTable
import random

# %%
# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

class Node:
    def __init__(self, url, contents, next, prev):
        self.url = url
        self.contents = contents
        self.next = next
        self.prev = prev


class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.n = n
        self.hash_table = HashTable()
        # rtype put() -> boolean
        # rtype get() -> (the value of the item, boolean)
        # rtype delete() -> boolean
        self.head = None
      
     

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        if self.hash_table.get(url)[1]:
            # 元々キャッシュリストの中に存在する時の話
            if self.head.url == url:
                return
            # Adjust the neighboring previous nodes
            item = self.head
            while item.next:
                prev_item = item
                item = item.next
                if item.url == url:
                    prev_item.next, item.next.prev = item.next, prev_item
                    break
            # Move the most recently accessed page to the head of the linked list            
            new_item = Node(url, contents, self.head, self.head.prev)
            self.head.prev.next = new_item
            self.head.prev = new_item
            self.head = new_item
            return
            
        else:
            #　Delete the oldest item
            if self.hash_table.size() == self.n:
                item = self.head.prev
                self.hash_table.delete(item.url)
                new_item = Node(url, contents, self.head, self.head.prev.prev)
                self.head.prev.prev.next = new_item
                self.head.prev = new_item
            # store this page
            elif self.head:
                new_item = Node(url, contents, self.head, self.head.prev)
                self.head.prev.next = new_item
                self.head.prev = new_item

            else:
                new_item = Node(url, contents, None, None)
                new_item.next = new_item
                new_item.prev = new_item 
            self.hash_table.put(url, contents)             
            self.head = new_item
            return
           
        # cache the url and contents properly


    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        item = self.head
        page_lists = []
        while item:
            page_lists.append(item.url)
            item = item.next
            if item == self.head:
                break
        return page_lists
        # return type : list[urls in order]


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]
    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]
    # Access "a.com" again.
    cache.access_page("a.com", "AAA") 
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]
    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Cache Tests passed!")

# キャッシュサイズが大きくなっても性能が落ちないかどうかチェック
def generate_large_cache_test(cache_class, cache_size=10000, num_accesses=100000):
    cache = cache_class(cache_size)
    urls = [f"page{i:05d}.com" for i in range(cache_size * 2)]  # 多めに用意

    start_time = time.perf_counter()
    start = start_time

    for i in range(num_accesses):
        # 80%の確率で既存URLを参照、20%で新規URLを投入
        if i < cache_size or random.random() < 0.2:
            url = random.choice(urls)
        else:
            url = f"page{random.randint(0, cache_size*2):05d}.com"
        contents = f"Contents of {url}"
        cache.access_page(url, contents)
        
        # 必要なら一部だけprint
        if i % 20000 == 0:
            print(f"Accessed {i} pages")
            end = time.perf_counter()
            diff = end - start
            print(f"Executed time : {diff}")
            start = end

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"\nLarge cache test completed!")
    print(f"Cache size: {cache_size}")
    print(f"Number of accesses: {num_accesses}")
    print(f"Execution time: {execution_time:.4f} seconds")
    
    # 最終結果表示（必要に応じて）
    pages = cache.get_pages()
    print(f"Number of pages stored in cache: {len(pages)}")
    print(f"Most recent pages (top 10): {pages[:10]}")


if __name__ == "__main__":
    start = time.perf_counter()
    cache_test()
    end = time.perf_counter()
    diff = end - start
    print(f"Execution time : {diff}")
    # generate_large_cache_test(Cache, cache_size=10000, num_accesses=100000)
    # %%
