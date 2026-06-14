"""
sorts.py
--------
The three sorting algorithms for my Computer Science Extended Essay.

  1. insertionSort  - simple sort, good for small arrays
  2. mergeSort       - divide-and-conquer sort, good for large arrays
  3. hybridSort      - merge sort that switches to insertion sort
                       once a part of the array is small enough
                       (the "cutoff threshold")

The research question is about how that cutoff threshold affects performance. 
The other two are baselines to compare against.

The insertionSort and mergeSort functions are based on the standard
implementations from GeeksforGeeks:
  - https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
  - https://www.geeksforgeeks.org/dsa/merge-sort/

All three rearrange the original array rather than returning a new one, 
though merge and hybrid use temporary arrays internally during merging. 
The index parameters (left, right) say which part of the array to work on.
"""


# ---------------------------------------------------------------------------
# 1. INSERTION SORT  (baseline)
# ---------------------------------------------------------------------------
def insertionSort(arr):
    """Sort the whole array using insertion sort.

    Idea: go through the array one item at a time. For each item,
    move it backwards until it sits in the right place among the
    items already sorted to its left.
    """
    for i in range(1, len(arr)):
        key = arr[i]      # the item we are placing
        j = i - 1         # the item just to its left

        # Move items that are bigger than key one step to the right,
        # to make room for key.
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        # Drop key into the gap we made.
        arr[j + 1] = key


# ---------------------------------------------------------------------------
# 2. MERGE SORT  (baseline)
# ---------------------------------------------------------------------------
def merge(arr, left, mid, right):
    """Merge two already-sorted parts of arr back together.

    The two parts are arr[left..mid] and arr[mid+1..right].
    """
    n1 = mid - left + 1   # size of the left part
    n2 = right - mid      # size of the right part

    # Copy the two parts into temporary arrays L and R.
    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]

    i = 0          # position in L
    j = 0          # position in R
    k = left       # position in arr where the next item goes

    # Repeatedly take the smaller front item and put it back in arr.
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # One part is now empty. Copy whatever is left of the other.
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def mergeSort(arr, left, right):
    """Sort arr[left..right] using merge sort.

    Idea: split the part in half, sort each half, then merge them.
    To sort a whole array, call mergeSort(arr, 0, len(arr) - 1).
    """
    if left < right:
        mid = (left + right) // 2
        mergeSort(arr, left, mid)        # sort the left half
        mergeSort(arr, mid + 1, right)   # sort the right half
        merge(arr, left, mid, right)     # merge the two halves


# ---------------------------------------------------------------------------
# 3. HYBRID SORT  (the one the essay is really about)
# ---------------------------------------------------------------------------
def insertionSortRange(arr, left, right):
    """Insertion sort, but only on the part arr[left..right].

    This is the same idea as insertionSort above. The hybrid needs it
    because it must sort small *parts* of the array, not the whole thing.
    """
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def hybridSort(arr, left, right, threshold):
    """Sort arr[left..right] using merge sort, but switch to insertion
    sort when the part is small.

    'threshold' is the size at or below which we stop splitting and use
    insertion sort instead. Trying different thresholds is the whole
    point of the experiment.
    To sort a whole array, call hybridSort(arr, 0, len(arr) - 1, threshold).
    """
    # How many items are in this part of the array.
    size = right - left + 1

    if size <= threshold:
        # Small part: insertion sort is usually faster here.
        insertionSortRange(arr, left, right)
    elif left < right:
        # Bigger part: behave like normal merge sort.
        mid = (left + right) // 2
        hybridSort(arr, left, mid, threshold)
        hybridSort(arr, mid + 1, right, threshold)
        merge(arr, left, mid, right)


# ---------------------------------------------------------------------------
# A utility function to print an array (from GeeksforGeeks)
# ---------------------------------------------------------------------------
def printArray(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()


# ---------------------------------------------------------------------------
# QUICK TESTS
# ---------------------------------------------------------------------------
# This block only runs when you run this file directly
# (e.g. "python sort_algorithms.py"). It lets me check the algorithms work
# before using them in the real experiment.
if __name__ == "__main__":
    original = [12, 11, 13, 5, 6, 38, 27, 43, 10, 3]
    correct = sorted(original)   # Python's built-in sort, the "right answer"

    print("Original array: ", end="")
    printArray(original)
    print("Correct answer: ", end="")
    printArray(correct)
    print()

    # Each sort changes the array it is given, so we give each one a
    # fresh copy (original[:]) of the unsorted array.

    arr1 = original[:]
    insertionSort(arr1)
    print("Insertion sort: ", end="")
    printArray(arr1)
    print("  correct?", arr1 == correct)

    arr2 = original[:]
    mergeSort(arr2, 0, len(arr2) - 1)
    print("Merge sort:     ", end="")
    printArray(arr2)
    print("  correct?", arr2 == correct)

    arr3 = original[:]
    hybridSort(arr3, 0, len(arr3) - 1, threshold=3)
    print("Hybrid sort:    ", end="")
    printArray(arr3)
    print("  correct?", arr3 == correct)
