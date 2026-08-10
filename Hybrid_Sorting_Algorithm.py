def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]

    i = 0
    j = 0
    k = left

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def insertionSortRange(arr, left, right):
    # basically the same as insertionSort but it only works on
    # part of the array (from left to right) not the whole thing
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def hybridSort(arr, left, right, threshold):
    size = right - left + 1

    # if the part we are sorting is small, just use insertion sort
    # since it does not have all the extra recursion/merging overhead
    if size <= threshold:
        insertionSortRange(arr, left, right)
    else:
        # otherwise keep splitting in half like normal merge sort
        if left < right:
            mid = (left + right) // 2
            hybridSort(arr, left, mid, threshold)
            hybridSort(arr, mid + 1, right, threshold)
            merge(arr, left, mid, right)