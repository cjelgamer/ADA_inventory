from datetime import datetime

def check_alerts(inventory):
    """Revisa productos cerca de caducar o que necesitan reabastecimiento"""
    today = datetime.today()

    for product in inventory.products:
        expiry_date = datetime.strptime(product.expiry_date, '%Y-%m-%d')
        days_to_expire = (expiry_date - today).days
        
        if days_to_expire <= 30:
            print(f"ALERTA: El producto {product.name} está cerca de su fecha de caducidad ({product.expiry_date}).")
        
        # Puedes agregar más condiciones, como alertas para reabastecimiento según la cantidad
