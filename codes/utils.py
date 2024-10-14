import os
import csv

def load_all_csv(directory):
    """Carga todos los archivos CSV de un directorio y retorna los productos en una lista"""
    products = []
    
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            category = file_name.replace('.csv', '')  # Eliminar la extensión para usarlo como categoría
            file_path = os.path.join(directory, file_name)
            
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product_data = {
                        'code': row.get('code'),
                        'name': row.get('name'),
                        'category': category,  # Asignar categoría desde el nombre del archivo
                        'price': float(row.get('price', 0)),
                        'entry_date': row.get('entry_date', '2024-01-01'),
                        'expiry_date': row.get('expiry_date', '2025-01-01'),
                        'stock': int(row.get('stock', 0))
                    }
                    products.append(product_data)
    
    return products
