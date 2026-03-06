class Heap:
    def __init__(self, arr):
        self.data = arr.copy()
        self._build_heap()
    
    def _build_heap(self):
        n = len(self.data)
        for i in range(n//2 - 1, -1, -1):
            self._sink(i, n)

    def _sink(self, i, n):
        while True:
            largest = i
            left = 2*i + 1
            right = 2*i + 2
            
            if left < n and self.data[left] > self.data[largest]:
                largest = left
            if right < n and self.data[right] > self.data[largest]:
                largest = right
            
            if largest == i:
                break
            
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest
    
    def __str__(self):
        return str(self.data)