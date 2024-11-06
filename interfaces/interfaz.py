import tkinter as tk
from tkinter import messagebox, simpledialog
from Juego import Triki, Serpiente, AdivinaNumero, PiedraPapelTijeras, Buscaminas


class InterfazJuegos:
    def __init__(self, root):
        self.root = root
        self.root.title("App de Juegos")
        self.root.config(bg="#333333")  # Fondo oscuro para el estilo moderno
        self.jugador_nombre = ""
        self.juego_actual = None
        self.crear_menu_inicio()

    def crear_menu_inicio(self):
        self.limpiar_ventana()

        # Encabezado
        encabezado = tk.Label(self.root, text="Bienvenido a la App de Juegos", font=('Helvetica', 18, 'bold'), bg="#333333",
                              fg="#f0a500")
        encabezado.pack(pady=20)

        # Botón de ingreso de nombre con estilo mejorado
        boton_nombre = tk.Button(self.root, text="Ingresar Nombre", command=self.ingresar_nombre,
                                 font=('Helvetica', 12), bg="#f0a500", fg="white", activebackground="#ffbc00",
                                 relief="raised")
        boton_nombre.pack(pady=20)

    def ingresar_nombre(self):
        self.jugador_nombre = simpledialog.askstring("Nombre del Jugador", "Por favor, ingresa tu nombre:")
        if self.jugador_nombre:
            self.mostrar_menu_juegos()

    def mostrar_menu_juegos(self):
        self.limpiar_ventana()

        # Título del menú de juegos
        etiqueta = tk.Label(self.root, text=f"Bienvenido, {self.jugador_nombre}. Selecciona un juego:",
                            font=('Helvetica', 14, 'bold'), bg="#333333", fg="#f0a500")
        etiqueta.pack(pady=20)

        # Frame para el menú de juegos
        frame_juegos = tk.Frame(self.root, bg="#444444", bd=2, relief="sunken")
        frame_juegos.pack(pady=10, padx=10, fill="both", expand=True)

        juegos = [
            ("Triki", Triki),
            ("Serpiente", Serpiente),
            ("Adivina el Número", AdivinaNumero),
            ("Piedra, Papel o Tijeras", PiedraPapelTijeras),
            ("Buscaminas", Buscaminas)
        ]

        # Crear botones de juegos con íconos y estilo mejorado
        for nombre, juego in juegos:
            boton = tk.Button(frame_juegos, text=nombre, font=('Helvetica', 12), bg="#4CAF50", fg="white",
                              activebackground="#388E3C", activeforeground="white", relief="ridge",
                              command=lambda j=juego: self.iniciar_juego(j))
            boton.pack(pady=10, fill="x", padx=20)

    def iniciar_juego(self, clase_juego):
        # Limpiamos la ventana y verificamos que clase_juego no sea None
        if clase_juego is not None:
            self.limpiar_ventana()
            self.juego_actual = clase_juego(self.root, self.volver_a_jugar_o_menu)
        else:
            messagebox.showerror("Error", "No se pudo iniciar el juego.")

    def volver_a_jugar_o_menu(self):
        # Diálogo para preguntar si quiere volver a jugar o ir al menú
        respuesta = messagebox.askyesno("Juego Terminado", "¿Quieres volver a jugar?")
        if respuesta:
            # Asegurarse de que el juego actual existe y es válido
            if self.juego_actual is not None:
                self.iniciar_juego(type(self.juego_actual))
            else:
                messagebox.showerror("Error", "El juego no se ha inicializado correctamente.")
        else:
            self.mostrar_menu_juegos()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Ejecución
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    root.config(bg="#333333")  # Fondo de la ventana principal en un tono oscuro
    app = InterfazJuegos(root)
    root.mainloop()
