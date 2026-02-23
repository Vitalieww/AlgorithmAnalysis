import math

def quicksort(arr):
    """In-place QuickSort using last element as pivot."""
    def _quicksort(low, high):
        if low < high:
            # Partition and get pivot index
            pivot_index = partition(low, high)
            # Recursively sort left and right
            _quicksort(low, pivot_index - 1)
            _quicksort(pivot_index + 1, high)

    def partition(low, high):
        pivot = arr[high]      # choose last element as pivot
        i = low - 1            # index of smaller element
        for j in range(low, high):
            if arr[j] < pivot: # if current element is smaller than pivot
                i += 1
                arr[i], arr[j] = arr[j], arr[i]  # swap
        arr[i + 1], arr[high] = arr[high], arr[i + 1]  # move pivot to correct position
        return i + 1

    _quicksort(0, len(arr) - 1)

def mergesort(arr):
    """In-place MergeSort implementation."""

    if len(arr) > 1:
        mid = len(arr) // 2

        # Split
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sort both halves
        mergesort(left_half)
        mergesort(right_half)

        # Merge step
        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copy remaining elements
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def heapsort(arr):
    """In-place HeapSort implementation."""

    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        # Move current root (largest) to end
        arr[i], arr[0] = arr[0], arr[i]
        # Restore heap property
        heapify(arr, i, 0)


def heapify(arr, n, i):
    """Ensure subtree rooted at index i is a max heap."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # If left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def introsort(arr):
    """IntroSort: hybrid of QuickSort and HeapSort."""

    max_depth = 2 * math.floor(math.log2(len(arr))) if len(arr) > 0 else 0

    def _introsort(low, high, depth_limit):
        if low < high:
            size = high - low + 1
            if depth_limit == 0:
                # Switch to HeapSort for this segment
                heapsort_segment(arr, low, high)
            else:
                # QuickSort partition
                pivot_index = partition(low, high)
                _introsort(low, pivot_index - 1, depth_limit - 1)
                _introsort(pivot_index + 1, high, depth_limit - 1)

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def heapsort_segment(a, start, end):
        """HeapSort only for a segment of array [start, end]."""
        n = end - start + 1

        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify_segment(a, n, i, start)

        # Extract elements
        for i in range(n - 1, 0, -1):
            a[start + i], a[start] = a[start], a[start + i]
            heapify_segment(a, i, 0, start)

    def heapify_segment(a, n, i, offset):
        """Heapify for segment starting at offset."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and a[offset + left] > a[offset + largest]:
            largest = left
        if right < n and a[offset + right] > a[offset + largest]:
            largest = right
        if largest != i:
            a[offset + i], a[offset + largest] = a[offset + largest], a[offset + i]
            heapify_segment(a, n, largest, offset)

    _introsort(0, len(arr) - 1, max_depth)