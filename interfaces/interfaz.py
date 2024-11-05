import tkinter as tk
from tkinter import messagebox, simpledialog
from Juego import Triki, Serpiente, AdivinaNumero, PiedraPapelTijeras, Buscaminas

class InterfazJuegos:
    def __init__(self, root):
        self.root = root
        self.jugador_nombre = ""
        self.juego_actual = None
        self.crear_menu_inicio()

    def crear_menu_inicio(self):
        self.limpiar_ventana()
        label = tk.Label(self.root, text="Bienvenido a la App de Juegos", font=('Arial', 16))
        label.pack(pady=10)

        boton_nombre = tk.Button(self.root, text="Ingresar Nombre", command=self.ingresar_nombre)
        boton_nombre.pack(pady=10)

    def ingresar_nombre(self):
        self.jugador_nombre = simpledialog.askstring("Nombre del Jugador", "Por favor, ingresa tu nombre:")
        if self.jugador_nombre:
            self.mostrar_menu_juegos()

    def mostrar_menu_juegos(self):
        self.limpiar_ventana()
        label = tk.Label(self.root, text=f"Bienvenido, {self.jugador_nombre}. Selecciona un juego:", font=('Arial', 14))
        label.pack(pady=10)

        juegos = [
            ("Triki", Triki),
            ("Serpiente", Serpiente),
            ("Adivina el Número", AdivinaNumero),
            ("Piedra, Papel o Tijeras", PiedraPapelTijeras),
            ("Buscaminas", Buscaminas)
        ]

        for nombre, juego in juegos:
            boton = tk.Button(self.root, text=nombre, command=lambda j=juego: self.iniciar_juego(j))
            boton.pack(pady=5)

    def iniciar_juego(self, juego_clase):
        self.limpiar_ventana()
        self.juego_actual = juego_clase(self.root, self.volver_a_jugar_o_menu)

    def volver_a_jugar_o_menu(self):
        respuesta = messagebox.askyesno("Juego Terminado", "¿Quieres volver a jugar?")
        if respuesta:
            self.iniciar_juego(type(self.juego_actual))
        else:
            self.mostrar_menu_juegos()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Ejecución
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = InterfazJuegos(root)
    root.mainloop()
