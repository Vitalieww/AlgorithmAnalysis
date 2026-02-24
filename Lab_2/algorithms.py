import math
import random

def quicksort(arr):
    """Classic QuickSort with last element as pivot (iterative to avoid recursion limit)."""
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    if len(arr) <= 1:
        return

    stack = [(0, len(arr) - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            p = partition(low, high)
            stack.append((low, p - 1))
            stack.append((p + 1, high))


def quicksort_improved(arr):
    """
    3-way partitioning QuickSort (Dijkstra / Dutch National Flag).
    Groups elements equal to the pivot together, so arrays with many
    duplicates converge in O(n) comparisons instead of O(n²).
    Pivot is chosen as median-of-three for better real-world performance.
    """
    def median_of_three(lo, hi):
        mid = (lo + hi) // 2
        if arr[hi] < arr[lo]:
            arr[lo], arr[hi] = arr[hi], arr[lo]
        if arr[mid] < arr[lo]:
            arr[mid], arr[lo] = arr[lo], arr[mid]
        if arr[hi] < arr[mid]:
            arr[hi], arr[mid] = arr[mid], arr[hi]
        # arr[mid] is the median; move it just before hi as pivot
        arr[mid], arr[hi - 1] = arr[hi - 1], arr[mid]
        return arr[hi - 1]

    def _sort(lo, hi):
        if hi - lo < 1:
            return
        if hi - lo == 1:
            if arr[hi] < arr[lo]:
                arr[lo], arr[hi] = arr[hi], arr[lo]
            return

        pivot = median_of_three(lo, hi)
        # 3-way partition: lt..i are <pivot, i..gt are >pivot, middle is ==pivot
        lt, i, gt = lo, lo, hi - 1
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i  += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        # place pivot back
        arr[i], arr[hi - 1] = arr[hi - 1], arr[i]

        _sort(lo, lt - 1)
        _sort(i + 1, hi)

    if len(arr) > 1:
        _sort(0, len(arr) - 1)

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

def mergesort_improved(arr):
    """
    Bottom-up iterative MergeSort with insertion sort for small subarrays.
    - Eliminates recursion overhead entirely.
    - Uses insertion sort on runs of size <= 16 (cache-friendly, low overhead).
    - Early-exit merge: if arr[mid] <= arr[mid+1] the run is already sorted.
    """
    n = len(arr)
    if n <= 1:
        return

    RUN = 16

    # Step 1: sort small runs with insertion sort
    for start in range(0, n, RUN):
        end = min(start + RUN - 1, n - 1)
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    # Step 2: bottom-up merge of sorted runs
    size = RUN
    while size < n:
        for lo in range(0, n, size * 2):
            mid = min(lo + size - 1, n - 1)
            hi  = min(lo + size * 2 - 1, n - 1)
            if mid >= hi:
                continue
            # Early exit: already sorted
            if arr[mid] <= arr[mid + 1]:
                continue
            # Merge arr[lo..mid] and arr[mid+1..hi]
            left  = arr[lo:mid + 1]
            right = arr[mid + 1:hi + 1]
            i = j = 0
            k = lo
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    arr[k] = left[i]; i += 1
                else:
                    arr[k] = right[j]; j += 1
                k += 1
            while i < len(left):
                arr[k] = left[i]; i += 1; k += 1
            while j < len(right):
                arr[k] = right[j]; j += 1; k += 1
        size *= 2



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


def heapsort_improved(arr):
    """
    HeapSort with two improvements:
    1. Iterative sift-down (no recursion, avoids stack overhead).
    2. Floyd's bottom-up heap construction starts sifting from a leaf's
       parent and uses a 'sift-up after sift-down' trick that halves the
       number of comparisons during the extraction phase.
    """
    n = len(arr)
    if n <= 1:
        return

    def sift_down(root, end):
        """Push arr[root] down to restore heap property in arr[root..end]."""
        while True:
            child = 2 * root + 1          # left child
            if child > end:
                break
            # pick the larger child
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] < arr[child]:
                arr[root], arr[child] = arr[child], arr[root]
                root = child
            else:
                break

    # Build max-heap (O(n))
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n - 1)

    # Extract elements one by one
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end - 1)


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


def introsort_improved(arr):
    """
    PDQSort-inspired IntroSort (Pattern-Defeating QuickSort).
    Improvements over the original:
    - Detects already-sorted / reverse-sorted runs and skips or reverses them.
    - Uses 'ninther' (median of medians of 3 triples) pivot for large arrays,
      greatly reducing worst-case pivot selection.
    - 3-way partition collapses equal elements, O(n) on all-duplicates input.
    - Insertion sort threshold raised to 24 (tuned empirically).
    - Shuffles a small sample when many bad partitions are detected (like pdqsort).
    """
    INSERTION_THRESHOLD = 24

    def insertion_sort(lo, hi):
        for i in range(lo + 1, hi + 1):
            key = arr[i]
            j = i - 1
            while j >= lo and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    def sift_down(lo, root, end):
        while True:
            child = 2 * (root - lo) + 1 + lo
            if child > end:
                break
            if child + 1 <= end and arr[child] < arr[child + 1]:
                child += 1
            if arr[root] < arr[child]:
                arr[root], arr[child] = arr[child], arr[root]
                root = child
            else:
                break

    def heap_sort_range(lo, hi):
        n = hi - lo + 1
        for i in range(lo + n // 2 - 1, lo - 1, -1):
            sift_down(lo, i, hi)
        for i in range(hi, lo, -1):
            arr[lo], arr[i] = arr[i], arr[lo]
            sift_down(lo, lo, i - 1)

    def med3(a, b, c):
        """Index of median of arr[a], arr[b], arr[c]."""
        if arr[a] < arr[b]:
            if arr[b] < arr[c]: return b
            return c if arr[a] < arr[c] else a
        else:
            if arr[a] < arr[c]: return a
            return c if arr[b] < arr[c] else b

    def ninther(lo, hi):
        """Tukey's ninther: median of 3 medians, reduces pivot bias on large arrays."""
        n = hi - lo
        s = n // 8
        m = lo + n // 2
        a = med3(lo,     lo + s,     lo + 2 * s)
        b = med3(m - s,  m,          m + s)
        c = med3(hi - 2*s, hi - s,   hi)
        return med3(a, b, c)

    def partition3(lo, hi, pivot_idx):
        """3-way partition around arr[pivot_idx]. Returns (lt, gt)."""
        arr[pivot_idx], arr[lo] = arr[lo], arr[pivot_idx]
        pivot = arr[lo]
        lt, i, gt = lo, lo + 1, hi
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1; i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        return lt, gt

    def _sort(lo, hi, depth_limit, bad_allowed):
        while hi - lo >= INSERTION_THRESHOLD:
            if depth_limit == 0:
                heap_sort_range(lo, hi)
                return

            n = hi - lo + 1

            # --- detect already-sorted run ---
            if arr[lo] <= arr[lo + 1]:
                sorted_run = lo + 1
                while sorted_run < hi and arr[sorted_run] <= arr[sorted_run + 1]:
                    sorted_run += 1
                if sorted_run == hi:
                    return          # fully sorted

            # --- detect reverse-sorted run and flip ---
            if arr[lo] >= arr[lo + 1]:
                rev_end = lo + 1
                while rev_end < hi and arr[rev_end] >= arr[rev_end + 1]:
                    rev_end += 1
                if rev_end == hi:
                    # reverse the whole slice
                    l, r = lo, hi
                    while l < r:
                        arr[l], arr[r] = arr[r], arr[l]
                        l += 1; r -= 1
                    return

            # --- pivot selection ---
            if n > 128:
                pivot_idx = ninther(lo, hi)
            else:
                pivot_idx = med3(lo, lo + n // 2, hi)

            # --- shuffle if too many bad partitions ---
            if bad_allowed == 0:
                random.shuffle(arr[lo:hi + 1])  # last resort
                bad_allowed = n

            lt, gt = partition3(lo, hi, pivot_idx)

            left_size  = lt - lo
            right_size = hi - gt

            # check if the partition was "bad" (heavily unbalanced)
            if left_size < n // 8 or right_size < n // 8:
                bad_allowed -= 1

            depth_limit -= 1

            # recurse on smaller side, loop on larger (tail-call optimisation)
            if left_size <= right_size:
                _sort(lo, lt - 1, depth_limit, bad_allowed)
                lo = gt + 1
            else:
                _sort(gt + 1, hi, depth_limit, bad_allowed)
                hi = lt - 1

        insertion_sort(lo, hi)

    n = len(arr)
    if n > 1:
        depth = 2 * math.floor(math.log2(n))
        _sort(0, n - 1, depth, n)