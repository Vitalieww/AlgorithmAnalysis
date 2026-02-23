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
    # to implement
    pass