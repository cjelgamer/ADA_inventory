import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from inventory import Inventario
from sorting import timed_quick_sort, timed_merge_sort
from product import Producto
from alert_manager import check_alerts
from datetime import datetime
from searching import binary_search, hash_search, binary_search_relocation, hash_search_relocation
import random
import time
import tracemalloc
from PIL import Image, ImageTk  # Para manejar la imagen del logo

class InventoryApp:
    def __init__(self, master):
        self.master = master
        self.inventory = Inventario()

        # Configuración para pantalla completa
        self.master.geometry("1200x700")
        self.master.state("zoomed")

        # Estilo de botones
        button_style = {"bg": "green", "fg": "white", "font": ("Arial", 12), "relief": "raised"}

        # Marco superior para botones
        top_frame = tk.Frame(master)
        top_frame.pack(pady=10)

        # Cargar el logo y colocarlo en la esquina superior derecha
        self.load_logo(top_frame)

        # Botones
        self.load_button = tk.Button(top_frame, text="Cargar CSV", command=self.load_csv, **button_style)
        self.load_button.grid(row=0, column=0, padx=10)

        self.add_button = tk.Button(top_frame, text="Agregar Producto", command=self.add_product_dialog, **button_style)
        self.add_button.grid(row=0, column=1, padx=10)

        self.reduce_button = tk.Button(top_frame, text="Reducir Cantidad", command=self.reduce_quantity_dialog, **button_style)
        self.reduce_button.grid(row=0, column=2, padx=10)

        self.delete_button = tk.Button(top_frame, text="Eliminar Producto", command=self.delete_product, bg="red", fg="white", font=("Arial", 12), relief="raised")
        self.delete_button.grid(row=0, column=3, padx=10)

        self.relocate_button = tk.Button(top_frame, text="Reubicar Productos", command=self.relocate_products, **button_style)
        self.relocate_button.grid(row=0, column=4, padx=10)

        # Botón para ajustar capacidad de estantes
        self.set_capacity_button = tk.Button(top_frame, text="Configurar Capacidad Estantes", command=self.set_shelves_capacity, **button_style)
        self.set_capacity_button.grid(row=0, column=5, padx=10)

        # Tabla para mostrar productos
        self.tree = ttk.Treeview(master, columns=("Nombre", "Precio", "Cantidad", "Fecha Expiración", "Estante"))
        self.tree.heading("#0", text="Código")
        self.tree.heading("#1", text="Nombre")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Fecha Expiración")
        self.tree.heading("#5", text="Estante")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Botones inferiores
        bottom_frame = tk.Frame(master)
        bottom_frame.pack(pady=10)

        self.report_expiring_button = tk.Button(bottom_frame, text="Reporte Próximos a Vencer", command=self.report_expiring_soon, **button_style)
        self.report_expiring_button.grid(row=0, column=0, padx=10)

        self.report_low_stock_button = tk.Button(bottom_frame, text="Reporte Productos Faltantes", command=self.report_low_stock, **button_style)
        self.report_low_stock_button.grid(row=0, column=1, padx=10)

        self.alert_button = tk.Button(bottom_frame, text="Ver Alertas", command=self.view_alerts, **button_style)
        self.alert_button.grid(row=0, column=2, padx=10)

        self.edit_button = tk.Button(bottom_frame, text="Editar Producto", command=self.edit_product_dialog, **button_style)
        self.edit_button.grid(row=0, column=3, padx=10)

        # Menú de selección de algoritmo de ordenamiento
        self.algorithm_var = tk.StringVar(value="quick_sort")
        self.algorithm_menu = ttk.Combobox(bottom_frame, textvariable=self.algorithm_var, values=['quick_sort', 'merge_sort'])
        self.algorithm_menu.grid(row=0, column=4, padx=10)

        # Menú de selección de algoritmo de búsqueda
        self.search_algorithm_var = tk.StringVar(value="binary_search")
        self.search_algorithm_menu = ttk.Combobox(bottom_frame, textvariable=self.search_algorithm_var, values=['binary_search', 'hash_search'])
        self.search_algorithm_menu.grid(row=0, column=5, padx=10)

        # Botón para ordenar productos
        self.sort_button = tk.Button(bottom_frame, text="Ordenar por Precio", command=self.sort_products, **button_style)
        self.sort_button.grid(row=0, column=6, padx=10)

        # Botón para buscar productos usando algoritmos de búsqueda
        self.search_button = tk.Button(bottom_frame, text="Buscar Producto", **button_style, command=self.search_product)
        self.search_button.grid(row=0, column=7, padx=10)

        # Texto para mostrar métricas de rendimiento
        self.metrics_label = tk.Label(bottom_frame, text="", font=("Arial", 10), fg="blue")
        self.metrics_label.grid(row=1, column=0, columnspan=8, pady=10)

    def load_logo(self, frame):
        try:
            logo = Image.open('logo.webp')  # Cargar la imagen del logo
            logo = logo.resize((70, 70), Image.LANCZOS)  # Redimensionar a 1cm * 1cm (aproximadamente 50x50 píxeles)
            self.logo_image = ImageTk.PhotoImage(logo)

            logo_label = tk.Label(frame, image=self.logo_image)
            logo_label.grid(row=0, column=6, padx=10, sticky='e')  # Colocar el logo en la esquina superior derecha
        except Exception as e:
            messagebox.showerror("Error al cargar el logo", str(e))

    # Cargar datos desde CSV
    def load_csv(self):
        file_path = 'Data/jugueteria.csv'  # Ajusta esto según tu archivo CSV
        self.inventory.load_from_csv(file_path)
        self.display_products()

    # Mostrar productos en la tabla
    def display_products(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for product in self.inventory.products:
            self.tree.insert("", "end", text=product.code, values=(product.name, product.price, product.stock, product.expiry_date, product.shelf))

    # Resto del código sigue igual...
    # (Aquí puedes pegar el resto de tu código, ya que no cambió)

    # Recuerda asegurarte de que la librería Pillow esté instalada:
    # Puedes instalarla usando pip:
    # pip install pillow


    # Función para agregar producto
    def add_product_dialog(self):
        self.add_window = tk.Toplevel(self.master)
        self.add_window.title("Agregar Producto")

        tk.Label(self.add_window, text="Código").pack()
        self.code_entry = tk.Entry(self.add_window)
        self.code_entry.pack()

        tk.Label(self.add_window, text="Nombre").pack()
        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.pack()

        tk.Label(self.add_window, text="Categoría").pack()
        self.category_entry = tk.Entry(self.add_window)
        self.category_entry.pack()

        tk.Label(self.add_window, text="Precio").pack()
        self.price_entry = tk.Entry(self.add_window)
        self.price_entry.pack()

        tk.Label(self.add_window, text="Fecha de Ingreso (YYYY-MM-DD)").pack()
        self.entry_date_entry = tk.Entry(self.add_window)
        self.entry_date_entry.pack()

        tk.Label(self.add_window, text="Fecha de Expiración (YYYY-MM-DD)").pack()
        self.expiry_date_entry = tk.Entry(self.add_window)
        self.expiry_date_entry.pack()

        tk.Label(self.add_window, text="Cantidad").pack()
        self.stock_entry = tk.Entry(self.add_window)
        self.stock_entry.pack()

        tk.Label(self.add_window, text="Unidad").pack()
        self.unit_entry = tk.Entry(self.add_window)
        self.unit_entry.pack()

        tk.Button(self.add_window, text="Agregar", command=self.save_product).pack()

    def save_product(self):
        new_product = Producto(
            self.code_entry.get(),
            self.name_entry.get(),
            self.category_entry.get(),
            float(self.price_entry.get()),
            self.entry_date_entry.get(),
            self.expiry_date_entry.get(),
            int(self.stock_entry.get()),
            self.unit_entry.get()
        )
        new_product.shelf = 0  # Colocar en almacén inicialmente
        self.inventory.add_product(new_product)
        self.add_window.destroy()
        self.display_products()

    # Función para reducir la cantidad de un producto
    def reduce_quantity_dialog(self):
        selected_item = self.tree.focus()
        if selected_item:
            product_code = self.tree.item(selected_item)['text']

            self.reduce_window = tk.Toplevel(self.master)
            self.reduce_window.title(f"Reducir cantidad del producto {product_code}")

            tk.Label(self.reduce_window, text="Cantidad a reducir").pack()
            self.reduce_entry = tk.Entry(self.reduce_window)
            self.reduce_entry.pack()

            tk.Button(self.reduce_window, text="Reducir", command=lambda: self.reduce_quantity(product_code)).pack()

    def reduce_quantity(self, product_code):
        reduce_by = int(self.reduce_entry.get())
        self.inventory.reduce_product_quantity(product_code, reduce_by)
        self.reduce_window.destroy()
        self.display_products()

    def edit_product_dialog(self):
        selected_item = self.tree.focus()
        if selected_item:
            product_code = self.tree.item(selected_item)['text']
            product = self.inventory.edit_product(product_code)  # Primero busca el producto por su código

            if product:
                self.edit_window = tk.Toplevel(self.master)
                self.edit_window.title(f"Editar {product.name}")

                tk.Label(self.edit_window, text="Nombre").pack()
                self.name_entry = tk.Entry(self.edit_window)
                self.name_entry.insert(0, product.name)
                self.name_entry.pack()

                tk.Label(self.edit_window, text="Precio").pack()
                self.price_entry = tk.Entry(self.edit_window)
                self.price_entry.insert(0, product.price)
                self.price_entry.pack()

                tk.Label(self.edit_window, text="Cantidad").pack()
                self.stock_entry = tk.Entry(self.edit_window)
                self.stock_entry.insert(0, product.stock)
                self.stock_entry.pack()

                tk.Button(self.edit_window, text="Guardar Cambios", command=lambda: self.save_product_changes(product_code)).pack()

    def save_product_changes(self, product_code):
        new_name = self.name_entry.get()
        new_price = float(self.price_entry.get())
        new_stock = int(self.stock_entry.get())

        # Actualizar el producto con los nuevos valores
        self.inventory.edit_product(product_code, new_name, new_price, new_stock)

        # Cerrar la ventana de edición
        self.edit_window.destroy()
        # Refrescar la vista para mostrar los cambios
        self.display_products()

    # Función para eliminar producto
    def delete_product(self):
        selected_item = self.tree.focus()
        if selected_item:
            product_code = self.tree.item(selected_item)['text']
            self.inventory.remove_product(product_code)
            self.display_products()

    # Función para reubicar productos en estantes
    def relocate_products(self):
        exec_time, memory_peak = self.inventory.assign_to_shelves_by_expiry()
        self.display_products()  # Actualiza la tabla con las nuevas ubicaciones de productos
    
        # Mostrar métricas de rendimiento
        self.metrics_label.config(text=f"Tiempo de ejecución: {exec_time:.6f} segundos | Pico de memoria: {memory_peak / 1024:.2f} KB")
    
        # Mostrar un mensaje de confirmación
        messagebox.showinfo("Reubicación Completa", "Los productos han sido reubicados según su fecha de expiración.")

    # Reporte de productos próximos a vencer
    def report_expiring_soon(self):
        search_algorithm = self.search_algorithm_var.get()

        if search_algorithm == "binary_search":
            # Ordenar por fecha de expiración antes de realizar la búsqueda binaria
            sorted_products = sorted(self.inventory.products, key=lambda p: p.expiry_date)
            soon_to_expire, exec_time, memory_peak = binary_search_relocation(sorted_products, days_left=30, key=lambda p: p.expiry_date)
        else:
            # Usar búsqueda por hash para fechas de expiración
            soon_to_expire, exec_time, memory_peak = hash_search_relocation(self.inventory.products, days_left=30, key=lambda p: p.expiry_date)

        if soon_to_expire:
            self.show_subwindow_report(soon_to_expire, "Productos Próximos a Vencer")
        else:
            messagebox.showinfo("Información", "No hay productos próximos a vencer")

        self.metrics_label.config(text=f"Tiempo de ejecución: {exec_time:.6f} segundos | Pico de memoria: {memory_peak / 1024:.2f} KB")

    # Reporte de productos con bajo stock
    def report_low_stock(self):
        search_algorithm = self.search_algorithm_var.get()

        if search_algorithm == "binary_search":
            # Ordenar los productos por su cantidad antes de realizar la búsqueda binaria
            sorted_products = sorted(self.inventory.products, key=lambda p: p.stock)
            low_stock, exec_time, memory_peak = binary_search_relocation(sorted_products, days_left=12, key=lambda p: p.stock)  # Usamos days_left como límite de stock
        else:
            # Usar búsqueda por hash para encontrar productos con bajo stock
            tracemalloc.start()  # Iniciar seguimiento de memoria
            start_time = time.time()  # Iniciar el temporizador
            low_stock = [product for product in self.inventory.products if product.stock < 12]  # Filtrar los productos con bajo stock
            end_time = time.time()  # Finalizar el temporizador
            memory_usage = tracemalloc.get_traced_memory()  # Obtener el uso de memoria
            tracemalloc.stop()  # Detener el seguimiento de memoria

            exec_time = end_time - start_time  # Calcular el tiempo de ejecución
            memory_peak = memory_usage[1]  # Obtener el pico de memoria

        if low_stock:
            self.show_subwindow_report(low_stock, "Productos Faltantes")
        else:
            messagebox.showinfo("Información", "No hay productos faltantes")

        self.metrics_label.config(text=f"Tiempo de ejecución: {exec_time:.6f} segundos | Pico de memoria: {memory_peak / 1024:.2f} KB")





    def show_subwindow_report(self, products, title):
        report_window = tk.Toplevel(self.master)
        report_window.title(title)

        report_tree = ttk.Treeview(report_window, columns=("Nombre", "Precio", "Cantidad", "Fecha Expiración", "Estante"))
        report_tree.heading("#0", text="Código")
        report_tree.heading("#1", text="Nombre")
        report_tree.heading("#2", text="Precio")
        report_tree.heading("#3", text="Cantidad")
        report_tree.heading("#4", text="Fecha Expiración")
        report_tree.heading("#5", text="Estante")
        report_tree.pack(pady=10, fill="both", expand=True)

        # Limpiar TreeView antes de insertar productos
        for product in products:
            report_tree.insert("", "end", text=product.code, values=(product.name, product.price, product.stock, product.expiry_date, product.shelf))

        close_button = tk.Button(report_window, text="Cerrar", command=report_window.destroy, bg="red", fg="white", font=("Arial", 12), relief="raised")
        close_button.pack(pady=10)


    def sort_products(self):
        algorithm = self.algorithm_var.get()
        if algorithm == "quick_sort":
            sorted_products, exec_time, memory_peak = timed_quick_sort(self.inventory.products, key=lambda p: p.price)
        else:
            sorted_products, exec_time, memory_peak = timed_merge_sort(self.inventory.products, key=lambda p: p.price)
        self.inventory.products = sorted_products
        self.display_products()
        self.metrics_label.config(text=f"Tiempo de ejecución: {exec_time:.6f} segundos | Pico de memoria: {memory_peak / 1024:.2f} KB")

    def search_product(self):
        search_code = simpledialog.askstring("Buscar Producto", "Ingresa el código del producto:")
        if search_code:
            search_algorithm = random.choice(['binary_search', 'hash_search'])

            if search_algorithm == "binary_search":
                # Ordenar la lista antes de la búsqueda binaria
                sorted_products = sorted(self.inventory.products, key=lambda p: p.code)
                result, exec_time, memory_peak = binary_search(sorted_products, search_code, key=lambda p: p.code)
            else:
                # Usar búsqueda por hash
                result, exec_time, memory_peak = hash_search(self.inventory.products, search_code)

            if result:
                self.show_subwindow_report([result], "Resultado de la Búsqueda")
                self.metrics_label.config(text=f"Tiempo de ejecución: {exec_time:.6f} segundos | Pico de memoria: {memory_peak / 1024:.2f} KB")
            else:
                messagebox.showinfo("Resultado", "Producto no encontrado")

    def set_shelves_capacity(self):
        capacity = simpledialog.askinteger("Capacidad Estantes", "Ingresa la capacidad para todos los estantes:")
        if capacity:
            self.inventory.set_all_shelves_capacity(capacity)
            messagebox.showinfo("Capacidad Estantes", f"Capacidad de todos los estantes ajustada a {capacity} productos.")

    def view_alerts(self):
        check_alerts(self.inventory)
