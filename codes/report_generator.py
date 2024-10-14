def generate_low_stock_report(products, threshold=10):
    report = "Productos con bajo stock:\n"
    for product in products:
        if product.stock <= threshold:
            report += f"{product.name} - Stock: {product.stock}\n"
    return report

def generate_soon_expiry_report(products, days_to_expire=30):
    import datetime
    today = datetime.date.today()
    report = "Productos próximos a vencer:\n"
    for product in products:
        expiry_date = datetime.datetime.strptime(product.expiry_date, "%Y-%m-%d").date()
        if (expiry_date - today).days <= days_to_expire:
            report += f"{product.name} - Fecha de expiración: {product.expiry_date}\n"
    return report
