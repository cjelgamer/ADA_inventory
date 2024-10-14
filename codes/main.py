from ui import InventoryApp
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Gestión de Inventarios")
    
    # Crear la aplicación
    app = InventoryApp(root)
    
    # Iniciar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
