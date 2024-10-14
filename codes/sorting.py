import time
import tracemalloc

def quick_sort(arr, key):
    if len(arr) <= 1:
        return arr
    pivot = key(arr[len(arr) // 2])
    left = [x for x in arr if key(x) < pivot]
    middle = [x for x in arr if key(x) == pivot]
    right = [x for x in arr if key(x) > pivot]
    return quick_sort(left, key) + middle + quick_sort(right, key)

def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = merge_sort(arr[:middle], key)
    right = merge_sort(arr[middle:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) < key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Funciones para medir el tiempo de ejecución y el uso de memoria
def timed_quick_sort(arr, key):
    tracemalloc.start()  # Inicia la medición de memoria
    start_time = time.time()  # Inicia la medición de tiempo

    sorted_arr = quick_sort(arr, key)

    end_time = time.time()  # Finaliza la medición de tiempo
    memory_usage = tracemalloc.get_traced_memory()  # Obtiene el uso de memoria
    tracemalloc.stop()  # Detiene la medición de memoria

    exec_time = end_time - start_time  # Calcula el tiempo de ejecución
    memory_peak = memory_usage[1]  # Obtiene el pico de memoria

    return sorted_arr, exec_time, memory_peak

def timed_merge_sort(arr, key):
    tracemalloc.start()  # Inicia la medición de memoria
    start_time = time.time()  # Inicia la medición de tiempo

    sorted_arr = merge_sort(arr, key)

    end_time = time.time()  # Finaliza la medición de tiempo
    memory_usage = tracemalloc.get_traced_memory()  # Obtiene el uso de memoria
    tracemalloc.stop()  # Detiene la medición de memoria

    exec_time = end_time - start_time  # Calcula el tiempo de ejecución
    memory_peak = memory_usage[1]  # Obtiene el pico de memoria

    return sorted_arr, exec_time, memory_peak
