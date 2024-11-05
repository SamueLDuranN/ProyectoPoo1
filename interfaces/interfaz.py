# interfaz.py
import tkinter as tk
from tkinter import messagebox
from Juego import Triki, Serpiente, AdivinaNumero, PiedraPapelTijeras, Buscaminas

class CasinoGames:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Games")
        self.root.geometry("600x600")
        self.root.configure(bg="#2c3e50")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        title = tk.Label(self.root, text="¡Bienvenido al Casino de Juegos!", font=('Arial', 24, 'bold'), bg="#2c3e50", fg="#ecf0f1")
        title.pack(pady=20)

        button_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 20,
            'height': 2,
            'bg': '#e74c3c',
            'fg': '#ecf0f1',
            'bd': 2,
            'relief': 'raised'
        }

        tk.Button(self.root, text="Triki", **button_style, command=self.jugar_triki).pack(pady=10)
        tk.Button(self.root, text="Serpiente", **button_style, command=self.jugar_serpiente).pack(pady=10)
        tk.Button(self.root, text="Adivina el Número", **button_style, command=self.jugar_adivina).pack(pady=10)
        tk.Button(self.root, text="Piedra, Papel o Tijeras", **button_style, command=self.jugar_piedra_papel).pack(pady=10)
        tk.Button(self.root, text="Buscaminas", **button_style, command=self.jugar_buscaminas).pack(pady=10)


    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def jugar_triki(self):
        self.clear_frame()
        Triki(self.root)

    def jugar_serpiente(self):
        self.clear_frame()
        Serpiente(self.root)

    def jugar_adivina(self):
        self.clear_frame()
        AdivinaNumero(self.root)

    def jugar_piedra_papel(self):
        self.clear_frame()
        PiedraPapelTijeras(self.root)

    def jugar_buscaminas(self):
        self.clear_frame()
        Buscaminas(self.root)




if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoGames(root)
    root.mainloop()
