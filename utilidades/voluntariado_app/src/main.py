"""
Punto de entrada del sistema de voluntariado y donaciones.
Ejecutar desde la carpeta raíz del proyecto:  python src/main.py
(En Linux puede ser python3 src/main.py)
"""

from db.conexion import probar_conexion


def main():
    ok, detalle = probar_conexion()
    if not ok:
        print("No se pudo conectar a MySQL:")
        print(detalle)
        print("\nRevise: 1) que MySQL esté iniciado, 2) los datos de src/config.py,")
        print("3) que haya ejecutado los scripts de la carpeta database/.")
        return

    print(f"Conexión exitosa. Versión de MySQL: {detalle}")

    # Prueba rápida de que Tkinter está instalado (en Linux: sudo apt install python3-tk)
    import tkinter as tk

    ventana = tk.Tk()
    ventana.title("Sistema de voluntariado y donaciones")
    ventana.geometry("420x160")
    tk.Label(ventana, text="Conexión exitosa a MySQL", font=("Arial", 14)).pack(pady=20)
    tk.Label(ventana, text="Aquí irá la pantalla de inicio.").pack()
    ventana.mainloop()


if __name__ == "__main__":
    main()
