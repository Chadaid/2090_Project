def heapi(arr, n, i):
    #Build a max heap
    largest = i          # Initialize the largest element as root
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    #If left child exists and is greater than the current largest node, update largest
    if left < n and arr[left] > arr[largest]:
        largest = left

    #If right child exists and is greater than the current largest node, update largest
    if right < n and arr[right] > arr[largest]:
        largest = right

    #If the largest element is not the current root node, swap
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # After swapping, the subtree may not satisfy the max heap property, so recursively adjust downward
        heapi(arr, n, largest)

def heap_sort(arr):

    #The main function of heap-sort
    n = len(arr)

    #Step 1: Build initial max heap
    #Start from the last non-leaf node and traverse backwards (index n//2 - 1)
    for i in range(n // 2 - 1, -1, -1):
        heapi(arr, n, i)
        
    print(f"Initial maximum heap: {arr}")

    #Step 2: Extract the largest element one by one and sort
    step = 1  # Step counter
    for i in range(n - 1, 0, -1):
        #Swap the current heap top to the end of the array
        arr[i], arr[0] = arr[0], arr[i]
        
        #Array state after each swap
        print(f"After the {step}th sort: {arr} (Sorted array: {arr[i:]})")
        step += 1
        
        #After swapping, adjust the new heap top to restore the max heap property
        heapi(arr, i, 0)

#Test code
if __name__ == "__main__":
    #1. Prepare an array
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"initial array: {arr}\n")

    #2. Heap sort
    heap_sort(arr)

    #3. Final result
    print(f"\nThe final result after heap-sort is completed: {arr}")
