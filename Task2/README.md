# Heap Sort

A Python implementation of **heap sort** using a max heap.

## How It Works
1. Build a max heap from the input array — $O(n)$
2. Repeatedly extract the max element and place it at the end — $O(n \log n)$

Overall time complexity: $O(n \log n)$

## How to Run
```bash
cd Task2
python "Heap sort.py"
```

### Example Output
```
initial array: [3, 1, 4, 1, 5, 9, 2, 6]

Initial maximum heap: [9, 6, 4, 1, 5, 3, 2, 1]
After the 1th sort: [6, 5, 4, 1, 1, 3, 2, 9] (Sorted array: [9])
...
The final result after heap-sort is completed: [1, 1, 2, 3, 4, 5, 6, 9]
```

## Introduction  Video
[Video](./Task2_video.mp4)