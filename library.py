def append_row(arr, width):
    internal_arr = []
    for j in range(width):
        internal_arr.append(0)
    arr.append(internal_arr)
    return arr


def concat_array_to_right(arr1, arr2):
    if len(arr1) < len(arr2):
        for i in range(len(arr2) - len(arr1)):
            arr1 = append_row(arr1, len(arr1[0]))
    for i in range(len(arr2)):
        for j in range(len(arr2[i])):
            arr1[i].append(arr2[i][j])
    return arr1


def concat_words(arr1, arr2):
    arr = []
    for i in range(len(arr1)):
        arr.append(arr1[i] + arr2[i])
    return arr


def append_column_left(arr):
    new_arr = []
    for i in range(len(arr)):
        new_arr.append([0])
        for j in range(len(arr[i])):
            new_arr[i].append(arr[i][j])
    return new_arr

def concat_array_to_bottom(arr1,arr2):
    for i in range(len(arr2)):
        arr1.append(arr2[i])
    return arr1
