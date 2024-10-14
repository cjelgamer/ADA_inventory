import time
import tracemalloc
import datetime

# Búsqueda binaria de productos por un atributo, como el código
def binary_search(arr, target, key):
    tracemalloc.start()  # Inicia la medición de memoria
    start_time = time.time()  # Inicia la medición de tiempo

    left, right = 0, len(arr) - 1
    result = None
    while left <= right:
        mid = (left + right) // 2
        if key(arr[mid]) == target:
            result = arr[mid]
            break
        elif key(arr[mid]) < target:
            left = mid + 1
        else:
            right = mid - 1

    end_time = time.time()  # Finaliza la medición de tiempo
    memory_usage = tracemalloc.get_traced_memory()  # Obtiene el uso de memoria
    tracemalloc.stop()  # Detiene la medición de memoria

    exec_time = end_time - start_time  # Calcula el tiempo de ejecución
    memory_peak = memory_usage[1]  # Obtiene el pico de memoria

    return result, exec_time, memory_peak

# Búsqueda por hash de productos (por código del producto)
def hash_search(products, product_code):
    tracemalloc.start()  # Inicia la medición de memoria
    start_time = time.time()  # Inicia la medición de tiempo

    product_dict = {product.code: product for product in products}
    result = product_dict.get(product_code, None)

    end_time = time.time()  # Finaliza la medición de tiempo
    memory_usage = tracemalloc.get_traced_memory()  # Obtiene el uso de memoria
    tracemalloc.stop()  # Detiene la medición de memoria

    exec_time = end_time - start_time  # Calcula el tiempo de ejecución
    memory_peak = memory_usage[1]  # Obtiene el pico de memoria

    return result, exec_time, memory_peak

# Búsqueda binaria de productos por atributo (por ejemplo, fecha de expiración o stock)
def binary_search_relocation(arr, days_left, key):
    tracemalloc.start()  # Inicia la medición de memoria
    start_time = time.time()  # Inicia la medición de tiempo

    soon_to_expire = []
    today = datetime.date.today()

    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        attribute_value = key(arr[mid])

        # Si el valor es una cadena de fecha
        if isinstance(attribute_value, str):
            expiry_date = datetime.datetime.strptime(attribute_value, "%Y-%m-%d").date()
            expiry_diff = (expiry_date - today).days

            # Verificar si está dentro del rango de días_left
            if 0 < expiry_diff <= days_left:
                soon_to_expire.append(arr[mid])

            if expiry_diff < days_left:
                left = mid + 1
            else:
                right = mid - 1

        # Si el valor es numérico (por ejemplo, para stock)
        elif isinstance(attribute_value, (int, float)):
            # En este caso, 'days_left' representa el límite inferior del stock
            if attribute_value < days_left:
                soon_to_expire.append(arr[mid])
            right -= 1  # Reducir el rango para continuar la búsqueda

    end_time = time.time()  # Finaliza la medición de tiempo
    memory_usage = tracemalloc.get_traced_memory()  # Obtiene el uso de memoria
    tracemalloc.stop()  # Detiene la medición de memoria

    exec_time = end_time - start_time  # Calcula el tiempo de ejecución
    memory_peak = memory_usage[1]  # Obtiene el pico de memoria

    return soon_to_expire, exec_time, memory_peak


# Búsqueda por hash de productos (por fecha de expiración o bajo stock)
def hash_search_relocation(products, days_left, key):
    tracemalloc.start()  # Inicia la medición de memoria
    start_time = time.time()  # Inicia la medición de tiempo

    soon_to_expire = []
    today = datetime.date.today()

    for product in products:
        attribute_value = key(product)

        # Si el valor es una cadena de fecha
        if isinstance(attribute_value, str):
            expiry_date = datetime.datetime.strptime(attribute_value, "%Y-%m-%d").date()
            expiry_diff = (expiry_date - today).days

            # Verificar si el producto vence dentro del rango
            if 0 < expiry_diff <= days_left:
                soon_to_expire.append(product)

        # Si el valor es numérico (stock)
        elif isinstance(attribute_value, (int, float)):
            # 'days_left' en este caso representa el límite de stock
            if attribute_value < days_left:
                soon_to_expire.append(product)

    end_time = time.time()  # Finaliza la medición de tiempo
    memory_usage = tracemalloc.get_traced_memory()  # Obtiene el uso de memoria
    tracemalloc.stop()  # Detiene la medición de memoria

    exec_time = end_time - start_time  # Calcula el tiempo de ejecución
    memory_peak = memory_usage[1]  # Obtiene el pico de memoria

    return soon_to_expire, exec_time, memory_peak
