class Producto:
    def __init__(self, code, name, category, price, entry_date, expiry_date, stock, unit, shelf=0):
        self.code = code
        self.name = name
        self.category = category
        self.price = price
        self.entry_date = entry_date
        self.expiry_date = expiry_date
        self.stock = stock
        self.unit = unit
        self.shelf = shelf  # Nuevo atributo para almacenar el número del estante

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.price} {self.unit} - Stock: {self.stock} - Estante: {self.shelf}"
