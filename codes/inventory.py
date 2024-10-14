from product import Producto
from searching import binary_search_relocation, hash_search_relocation, binary_search, hash_search
from sorting import quick_sort, merge_sort
import datetime
import time
import tracemalloc

class Inventario:
    def __init__(self):
        self.products = []
        self.shelves = [[] for _ in range(30)]  # Hasta 30 estantes disponibles
        self.max_capacity = {i: 10 for i in range(1, 31)}  # Capacidad máxima de cada estante (inicialmente 10)

        # Diccionario actualizado para convertir nombres completos en códigos de categoría
        self.category_mapping = {
            'Abarrotes': 'ABA',
            'Bebidas': 'BEB',
            'Carnes, Aves y Pescados': 'CAR',
            'Congelados': 'CON',
            'Cuidado del bebe': 'BBE',
            'Cuidado personal': 'CUP',
            'Frutas y verduras': 'FRU',
            'Jugueteria': 'JUG',
            'Lacteos y huevos': 'LAH',
            'Libreria': 'LIB',
            'Limpieza': 'LIM',
            'Mascotas': 'MAS',
            'Panaderia': 'PPC',
            'Quesos y fiambres': 'QF'
        }

        # Diccionario para definir el rango de estantes por código de categoría
        self.shelf_ranges = {
            'ABA': (1, 2, 3),
            'BEB': (4, 5),
            'CAR': (6, 7),
            'CON': (8, 9),
            'BBE': (10, 11),
            'CUP': (12, 13),
            'FRU': (14, 15),
            'JUG': (16, 17),
            'LAH': (18, 19),
            'LIB': (20, 21),
            'LIM': (22, 23),
            'MAS': (24, 25),
            'PPC': (26, 27),
            'QF': (28, 29)
        }

        # Parámetro para elegir el algoritmo de búsqueda ('binary_search_relocation' o 'hash_search_relocation')
        self.search_algorithm_relocation = 'binary_search_relocation'

    def set_all_shelves_capacity(self, capacity):
        # Establecer la misma capacidad para todos los estantes
        for shelf_number in self.max_capacity:
            self.max_capacity[shelf_number] = capacity

    def add_product(self, product):
        # Convertir el nombre de la categoría al código de categoría usando el mapeo
        product.category = self.category_mapping.get(product.category, product.category)
        self.products.append(product)

    def sort_products_by_expiry(self):
        # Ordenar productos por fecha de expiración usando quick_sort o merge_sort
        sorted_products, exec_time, memory_peak = quick_sort(self.products, key=lambda p: p.expiry_date)
        print(f"Productos ordenados por fecha de expiración en {exec_time} segundos, con un pico de memoria de {memory_peak} bytes")
        return sorted_products

    def assign_to_shelves_by_expiry(self):
        today = datetime.date.today()

        # Seleccionar el algoritmo de búsqueda para reubicación
        if self.search_algorithm_relocation == 'binary_search_relocation':
            soon_to_expire, exec_time, memory_peak = binary_search_relocation(self.products, days_left=50, key=lambda p: p.expiry_date)
        else:
            soon_to_expire, exec_time, memory_peak = hash_search_relocation(self.products, days_left=50)

        print(f"Reubicación completada en {exec_time} segundos, con un pico de memoria de {memory_peak} bytes")

        # Limpiar estantes
        self.shelves = [[] for _ in range(30)]  # Resetear estantes

        for product in self.products:
            expiry_date_diff = (datetime.datetime.strptime(product.expiry_date, "%Y-%m-%d").date() - today).days
            category_code = product.category

            # Verificar si el código de categoría es válido
            if category_code in self.shelf_ranges:
                shelf_range = self.shelf_ranges[category_code]

                # Asignar estante basado en proximidad de vencimiento
                if expiry_date_diff <= 30:
                    self.assign_to_shelf(product, shelf_range[0])  # Estante más cercano
                elif 30 < expiry_date_diff <= 80:
                    self.assign_to_shelf(product, shelf_range[1])  # Estante intermedio
                else:
                    self.assign_to_shelf(product, shelf_range[2] if len(shelf_range) > 2 else shelf_range[1])

        return exec_time, memory_peak

    def assign_to_shelf(self, product, shelf_number):
        remaining_stock = product.stock  # Cantidad total de stock del producto

        while remaining_stock > 0:
            # Espacio disponible en el estante actual
            available_space = self.max_capacity[shelf_number] - len(self.shelves[shelf_number - 1])

            if available_space > 0:
                # Cantidad que podemos mover al estante actual
                quantity_to_assign = min(available_space, remaining_stock)

                # Asignar el producto al estante (sin crear uno nuevo)
                product.stock = quantity_to_assign  # Reducir el stock según el estante
                product.shelf = shelf_number  # Actualizar el estante del producto

                # Añadir al estante
                self.shelves[shelf_number - 1].append(product)

                # Reducir el stock restante
                remaining_stock -= quantity_to_assign
            else:
                print(f"Estante {shelf_number} está lleno. Producto {product.name} no puede ser asignado completamente.")
                break

    def remove_product(self, product_code):
        # Filtrar la lista de productos para eliminar el producto con el código dado
        self.products = [product for product in self.products if product.code != product_code]

        # Eliminar también de los estantes si es necesario
        for shelf in self.shelves:
            shelf[:] = [product for product in shelf if product.code != product_code]

    def display_inventory(self):
        for shelf_num, shelf in enumerate(self.shelves):
            if shelf:
                print(f"Estante {shelf_num + 1}:")
                for product in shelf:
                    print(f"  - {product.name} (Código: {product.code}, Cantidad: {product.stock}, Vencimiento: {product.expiry_date}, Estante: {product.shelf})")

    def load_from_csv(self, file_path):
        import csv
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Producto(
                    row['code'], 
                    row['name'], 
                    row['category'], 
                    float(row['price']),  # Precio en formato float
                    row['entry_date'], 
                    row['expiry_date'], 
                    float(row['stock']),  # Cambia de int a float para manejar valores decimales
                    row['unit']
                )
                product.shelf = 0  # Inicialmente todos los productos empiezan en el almacén (shelf 0)
                self.add_product(product)


    def edit_product(self, product_code, new_name=None, new_price=None, new_stock=None):
        # Buscar el producto con el código especificado
        for product in self.products:
            if product.code == product_code:
                # Actualizar los atributos si se proporciona un valor nuevo
                if new_name:
                    product.name = new_name
                if new_price is not None:
                    product.price = new_price
                if new_stock is not None:
                    product.stock = new_stock
                return product  # Devolver el producto actualizado
        return None  # Si no se encuentra el producto
    



    # Función para descargar los productos en un archivo CSV
    def download_csv(self, file_path='inventario_descargado.csv'):
        import csv
        # Ordenar los productos por precio antes de descargar
        sorted_products = sorted(self.products, key=lambda p: p.price)

        # Escribir los productos en un archivo CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Código", "Nombre", "Precio", "Cantidad", "Fecha Expiración", "Estante"])
            for product in sorted_products:
                writer.writerow([product.code, product.name, product.price, product.stock, product.expiry_date, product.shelf])
        
        print(f"Inventario descargado en {file_path}")