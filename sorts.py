"""
sorts.py
--------
The three sorting algorithms for my Computer Science Extended Essay.

  1. insertion_sort  - simple sort, good for small lists
  2. merge_sort      - divide-and-conquer sort, good for large lists
  3. hybrid_sort     - merge sort that switches to insertion sort
                       once a sublist is small enough (the "threshold")

The research question is about how that threshold affects performance,
so the hybrid is the important one. The other two are baselines to
compare against.
"""


# ---------------------------------------------------------------------------
# 1. INSERTION SORT
# ---------------------------------------------------------------------------
def insertion_sort(numbers):
    """Sort a list of numbers using insertion sort.

    Idea: go through the list one item at a time. For each item,
    move it backwards until it sits in the right place among the
    items already sorted to its left.
    """
    # Start at the second item (index 1). The first item is a
    # sorted list of length 1 on its own.
    for i in range(1, len(numbers)):
        current = numbers[i]      # the item we are placing
        j = i - 1                 # the item just to its left

        # Shift bigger items one step to the right to make room.
        while j >= 0 and numbers[j] > current:
            numbers[j + 1] = numbers[j]
            j = j - 1

        # Drop the current item into the gap we made.
        numbers[j + 1] = current

    return numbers


# ---------------------------------------------------------------------------
# 2. MERGE SORT
# ---------------------------------------------------------------------------
def merge_sort(numbers):
    """Sort a list of numbers using merge sort.

    Idea: split the list in half, sort each half, then merge the
    two sorted halves back together.
    """
    # A list of 0 or 1 items is already sorted, so just return it.
    if len(numbers) <= 1:
        return numbers

    # Split the list into two halves.
    middle = len(numbers) // 2
    left_half = numbers[:middle]
    right_half = numbers[middle:]

    # Sort each half (this calls merge_sort again on smaller lists).
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # Merge the two sorted halves and return the result.
    return merge(left_half, right_half)


def merge(left, right):
    """Combine two already-sorted lists into one sorted list."""
    result = []
    i = 0   # position in the left list
    j = 0   # position in the right list

    # Keep taking the smaller front item until one list runs out.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1

    # One list is now empty. Add whatever is left of the other.
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ---------------------------------------------------------------------------
# 3. HYBRID SORT  (the one the essay is really about)
# ---------------------------------------------------------------------------
def hybrid_sort(numbers, threshold):
    """Sort using merge sort, but switch to insertion sort for
    small sublists.

    'threshold' is the size at or below which we stop splitting
    and use insertion sort instead. Trying different thresholds
    is the whole point of the experiment.
    """
    # If the list is small enough, insertion sort is usually faster,
    # so use it instead of splitting further.
    if len(numbers) <= threshold:
        return insertion_sort(numbers)

    # Otherwise behave like normal merge sort.
    middle = len(numbers) // 2
    left_half = numbers[:middle]
    right_half = numbers[middle:]

    left_half = hybrid_sort(left_half, threshold)
    right_half = hybrid_sort(right_half, threshold)

    return merge(left_half, right_half)


# ---------------------------------------------------------------------------
# QUICK TESTS
# ---------------------------------------------------------------------------
# This block only runs when you run this file directly
# (e.g. "python sorts.py"). It lets me check the algorithms work
# before using them in the real experiment.
if __name__ == "__main__":
    test_list = [5, 2, 9, 1, 5, 6, 3, 8, 0, 7]
    correct = sorted(test_list)   # Python's built-in sort, the "right answer"

    print("Original list:  ", test_list)
    print("Correct answer: ", correct)
    print()

    # We pass a copy (test_list[:]) so each sort gets the original
    # unsorted list, not one that a previous sort already changed.
    print("Insertion sort: ", insertion_sort(test_list[:]))
    print("Merge sort:     ", merge_sort(test_list[:]))
    print("Hybrid sort:    ", hybrid_sort(test_list[:], threshold=4))
    print()

    # Automatic checks: each result should equal the correct answer.
    print("Insertion correct?", insertion_sort(test_list[:]) == correct)
    print("Merge correct?    ", merge_sort(test_list[:]) == correct)
    print("Hybrid correct?   ", hybrid_sort(test_list[:], threshold=4) == correct)
