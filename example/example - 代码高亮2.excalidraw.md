---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


# Excalidraw Data

## Text Elements
from typing import List, Optional
import time

def timer_decorator(func):
    """这是一个用于测试文档字符串颜色的注释"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time: {time.time() - start:.4f}s")
        return result
    return wrapper

class DataProcessor:
    def __init__(self, data: List[int]):
        self.data = data

    @timer_decorator
    def process_evens(self) -> List[int]:
        # 测试列表推导式和取模运算的高亮
        return [x * 2 for x in self.data if x % 2 == 0]

if __name__ == "__main__":
    processor = DataProcessor([1, 2, 3, 4, 5])
    print(processor.process_evens())
    123123123
    3453453466
 ^M4CmYzTu

#include <stdio.h>
#include <stdlib.h>

#define MAX_BUFFER 1024

// 定义链表节点结构体
typedef struct Node {
    int data;
    struct Node* next;
} Node;

Node* create_node(int data) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    new_node->data = data; // 测试箭头操作符
    new_node->next = NULL;
    return new_node;
}

int main() {
    int values[] = {10, 20, 30};
    Node* head = create_node(values[0]);
    
    printf("Head node created with data: %d\n", head->data);
    free(head);
    return -1;
}
 ^nGV8Mtmf

const API_URL = "https://api.example.com/data";

// 模拟异步获取数据的函数
const fetchData = async (id) => {
    try {
        console.log(`Fetching data for ID: ${id}...`); // 模板字符串测试
        
        const response = await new Promise((resolve) => {
            setTimeout(() => {
                resolve({ id: id, status: "active", tags: ["js", "test"] });
            }, 1000);
        });

        return response;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

// 使用 Map 和解构赋值
const processUsers = (users) => {
    return users.map(({ id, name }) => {
        return {
            uniqueKey: `${id}-${name.toLowerCase()}`,
            isActive: true
        };
    });
};
 ^VFetha0p

const API_URL = "https://api.example.com/data";

// 模拟异步获取数据的函数
const fetchData = async (id) => {
    try {
        console.log(`Fetching data for ID: ${id}...`); // 模板字符串测试
        
        const response = await new Promise((resolve) => {
            setTimeout(() => {
                resolve({ id: id, status: "active", tags: ["js", "test"] });
            }, 1000);
        });

        return response;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

// 使用 Map 和解构赋值
const processUsers = (users) => {
    return users.map(({ id, name }) => {
        return {
            uniqueKey: `${id}-${name.toLowerCase()}`,
            isActive: true
        };
    });
};
 ^Fk8imbH9


## Tags
%%
## Drawing
```compressed-json
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
```
%%