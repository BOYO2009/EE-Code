# experiment.py
# First tests: measure the time and memory of insertion sort and merge sort.
# Usage:
#   python3 experiment.py 1000
#   python3 experiment.py 5000


import sys
import random
import time
import tracemalloc

from sort_algorithms import insertionSort, mergeSort


# Settings
INPUT_SIZE = 1000   # default number of integers to sort
INPUT_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else INPUT_SIZE   # number of integers to sort (from command line)


# Make a list of random integers
def make_random_array(size):
    arr = []
    for i in range(size):
        number = random.randint(0, 10000)
        arr.append(number)
    return arr


# Print a header line so the output is easy to copy into the CSV
print("algorithm,input_size,time_ms,peak_memory_bytes")

# Make one random list to sort
data = make_random_array(INPUT_SIZE)

# ----- Insertion sort -----

# Measure time
arr = data[:]                 # copy of the unsorted list
start = time.perf_counter()
insertionSort(arr)
end = time.perf_counter()
insertion_time = round((end - start) * 1000, 3) # convert to milliseconds and round to 3rd decimal places

# Measure memory (separate run, so the timer above stays accurate)
arr = data[:]
tracemalloc.start()
insertionSort(arr)
current_memory, insertion_peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("insertion_sort," + str(INPUT_SIZE) + ","
      + str(insertion_time) + "," + str(insertion_peak_memory))

# ----- Merge sort -----

# Measure time
arr = data[:]
start = time.perf_counter()
mergeSort(arr, 0, len(arr) - 1)
end = time.perf_counter()
merge_time = round((end - start) * 1000, 3) # convert to milliseconds and round to 3rd decimal places
 
# Measure memory (separate run)
arr = data[:]
tracemalloc.start()
mergeSort(arr, 0, len(arr) - 1)
current_memory, merge_peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("merge_sort," + str(INPUT_SIZE) + ","
      + str(merge_time) + "," + str(merge_peak_memory))
