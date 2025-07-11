//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next; // pointer的な役割
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//



void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  metadata->next = my_heap.free_head;
  my_heap.free_head = metadata;

}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head = metadata->next;
    // .が普通
    // *で宣言しているから、pointerになっている
    // 
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}



// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  // Add a check for huge allocation requests to prevent infinite loops.
  if (size > 4096 - sizeof(my_metadata_t)) {
    // This simple allocator cannot handle requests larger than a page.
    return NULL; 
  }

  while (1) {
    // Variables to find the best-fit block
    my_metadata_t *best_fit = NULL; // どこにいるのか、pointer
    my_metadata_t *best_fit_prev = NULL;
    // Variables to iterate through the free list
    my_metadata_t *current = my_heap.free_head;
    my_metadata_t *current_prev = NULL;

    // Best-fit: Find the smallest free slot that the object fits.
    while (current) {
      if (current->size >= size) {
        if (best_fit == NULL || current->size < best_fit->size) {
          best_fit = current;
          best_fit_prev = current_prev;
        }
      }
      current_prev = current;
      current = current->next;
    }

    // If a suitable block was found
    if (best_fit) {
      void *ptr = best_fit + 1; //単純な隣というか、my_metadata一個分のbyte数離れた隣
      // 単純な隣だと、my_metadataの中身の情報を書き換えてしまうかもしれない
      size_t remaining_size = best_fit->size - size;
      my_remove_from_free_list(best_fit, best_fit_prev);

      if (remaining_size > sizeof(my_metadata_t)) {
        best_fit->size = size;
        my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
        new_metadata->size = remaining_size - sizeof(my_metadata_t);
        new_metadata->next = NULL;
        my_add_to_free_list(new_metadata);
      }
      return ptr;
    }

    // If no suitable block was found, allocate a new page from the system.
    size_t buffer_size = 4096;
    my_metadata_t *new_page = (my_metadata_t *)mmap_from_system(buffer_size);
    new_page->size = buffer_size - sizeof(my_metadata_t);
    new_page->next = NULL;
    my_add_to_free_list(new_page);
    // The while(1) loop will repeat, find the new page, and allocate from it.
  }
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;

  // 右側結合
  // メタデータ + ユーザーデータ領域 の隣が、次のメタデータのはず
  my_metadata_t *next_block_metadata = (my_metadata_t *)((char *)ptr + metadata->size);
  my_metadata_t *current = my_heap.free_head;
  my_metadata_t *prev = NULL;
  while (current) {
    if (current == next_block_metadata) {
      // 解放するブロックのサイズを、右ブロックのサイズと右ブロックのメタデータサイズ分だけ増やす
      metadata->size += sizeof(my_metadata_t) + current->size;
      // 右ブロックをフリーリストから削除する
      my_remove_from_free_list(current, prev);
      // マージは一度だけなのでループを抜ける
      break;
    }
    prev = current;
    current = current->next;
  }
  
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
