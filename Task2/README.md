# Simple Max Heap

This is a simple Python Max Heap class. It takes an unordered list and automatically converts it into a max heap upon initialization with a time complexity of $O(n)$.

## Usage

You can directly include or import this class into your code and pass a list to instantiate a max heap.

### Example

```python
# Assuming the code is saved in heap.py
# from heap import Heap

# 1. Prepare an unordered array
arr =[3, 1, 4, 1, 5, 9, 2, 6]

# 2. Instantiate the Heap
max_heap = Heap(arr)

# 3. Print the result
print(max_heap) 
# Output:[9, 6, 4, 1, 5, 3, 2, 1] 
# (The array now satisfies the max heap property: the parent node is always greater than or equal to its children)
