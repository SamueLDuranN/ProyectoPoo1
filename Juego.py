import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Triki:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.jugador_actual = "X"
        self.tablero = [[None for _ in range(3)] for _ in range(3)]
        self.crear_interfaz_triki()

    def crear_interfaz_triki(self):
        try:
            for i in range(3):
                for j in range(3):
                    boton = tk.Button(
                        self.root,
                        text="",
                        font=("Arial", 24, "bold"),
                        width=5,
                        height=2,
                        bg="#dfe6e9",
                        fg="#2d3436",
                        activebackground="#b2bec3",
                        relief="groove",
                        bd=3,
                        command=lambda i=i, j=j: self.marcar_casilla(i, j)
                    )
                    boton.grid(row=i, column=j, padx=5, pady=5)
                    self.tablero[i][j] = boton
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la interfaz del juego Triki: {e}")

    def marcar_casilla(self, i, j):
        try:
            if self.tablero[i][j]["text"] == "":
                self.tablero[i][j]["text"] = self.jugador_actual
                self.tablero[i][j]["fg"] = "#d63031" if self.jugador_actual == "X" else "#0984e3"
                if self.verificar_ganador():
                    messagebox.showinfo("Juego terminado", f"¡{self.jugador_actual} gana!")
                    self.callback_fin_juego()
                elif all(self.tablero[x][y]["text"] != "" for x in range(3) for y in range(3)):
                    messagebox.showinfo("Juego terminado", "¡Es un empate!")
                    self.callback_fin_juego()
                else:
                    self.jugador_actual = "O" if self.jugador_actual == "X" else "X"
        except Exception as e:
            messagebox.showerror("Error", f"Error al marcar la casilla: {e}")

    def verificar_ganador(self):
        try:
            for i in range(3):
                if self.tablero[i][0]["text"] == self.tablero[i][1]["text"] == self.tablero[i][2]["text"] != "":
                    return True
                if self.tablero[0][i]["text"] == self.tablero[1][i]["text"] == self.tablero[2][i]["text"] != "":
                    return True
            if self.tablero[0][0]["text"] == self.tablero[1][1]["text"] == self.tablero[2][2]["text"] != "":
                return True
            if self.tablero[0][2]["text"] == self.tablero[1][1]["text"] == self.tablero[2][0]["text"] != "":
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar el ganador: {e}")
            return False

class Serpiente:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.canvas = tk.Canvas(self.root, bg="black", width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.snake = [(250, 250), (240, 250), (230, 250)]
        self.direction = 'Right'
        self.food = None
        self.root.update()
        self.colocar_comida()

        self.mover_serpiente()
        self.root.bind("<KeyPress>", self.cambiar_direccion)
        self.root.bind("<Configure>", self.al_redimensionar)

    def al_redimensionar(self, event):
        try:
            self.canvas.config(width=event.width, height=event.height)
            if self.food is None or not (0 <= self.food[0] < event.width and 0 <= self.food[1] < event.height):
                self.colocar_comida()
        except Exception as e:
            messagebox.showerror("Error", f"Error al redimensionar la ventana: {e}")

    def colocar_comida(self):
        try:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            if width > 0 and height > 0:
                x = random.randint(0, (width // 10) - 1) * 10
                y = random.randint(0, (height // 10) - 1) * 10
                self.food = (x, y)
            else:
                self.root.after(100, self.colocar_comida)
        except Exception as e:
            messagebox.showerror("Error", f"Error al colocar la comida: {e}")

    def cambiar_direccion(self, event):
        try:
            nueva_direccion = event.keysym
            direcciones = {'Left', 'Right', 'Up', 'Down'}
            direcciones_opuestas = {('Left', 'Right'), ('Right', 'Left'), ('Up', 'Down'), ('Down', 'Up')}

            if nueva_direccion in direcciones and (self.direction, nueva_direccion) not in direcciones_opuestas:
                self.direction = nueva_direccion
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar la dirección: {e}")

    def mover_serpiente(self):
        try:
            cabeza_x, cabeza_y = self.snake[0]

            if self.direction == 'Left':
                cabeza_x -= 10
            elif self.direction == 'Right':
                cabeza_x += 10
            elif self.direction == 'Up':
                cabeza_y -= 10
            elif self.direction == 'Down':
                cabeza_y += 10

            nueva_cabeza = (cabeza_x, cabeza_y)

            if nueva_cabeza == self.food:
                self.colocar_comida()
            else:
                self.snake.pop()

            if (cabeza_x < 0 or cabeza_x >= self.canvas.winfo_width() or
                    cabeza_y < 0 or cabeza_y >= self.canvas.winfo_height() or nueva_cabeza in self.snake):
                messagebox.showinfo("Serpiente", "¡Perdiste!")
                self.callback_fin_juego()
                return

            self.snake.insert(0, nueva_cabeza)
            self.actualizar_canvas()
            self.root.after(100, self.mover_serpiente)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mover la serpiente: {e}")

    def actualizar_canvas(self):
        try:
            self.canvas.delete("all")
            for segmento in self.snake:
                self.canvas.create_rectangle(segmento[0], segmento[1], segmento[0] + 10, segmento[1] + 10, fill="green")
            self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el canvas: {e}")

class AdivinaNumero:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.numero_objetivo = random.randint(1, 100)
        self.pedir_adivinanza()

    def pedir_adivinanza(self):
        try:
            adivinanza = simpledialog.askinteger("Adivina el Número", "Adivina un número entre 1 y 100:")
            if adivinanza is None:
                self.callback_fin_juego()
            else:
                self.verificar_adivinanza(adivinanza)
        except Exception as e:
            messagebox.showerror("Error", f"Error al pedir la adivinanza: {e}")

    def verificar_adivinanza(self, adivinanza):
        try:
            if adivinanza < self.numero_objetivo:
                messagebox.showinfo("Resultado", "Demasiado bajo. ¡Inténtalo de nuevo!")
                self.pedir_adivinanza()
            elif adivinanza > self.numero_objetivo:
                messagebox.showinfo("Resultado", "Demasiado alto. ¡Inténtalo de nuevo!")
                self.pedir_adivinanza()
            else:
                messagebox.showinfo("Resultado", "¡Felicidades! Adivinaste el número.")
                self.callback_fin_juego()
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar la adivinanza: {e}")

class PiedraPapelTijeras:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.crear_interfaz_piedra_papel_tijeras()

    def crear_interfaz_piedra_papel_tijeras(self):
        try:
            self.root.title("Piedra, Papel o Tijeras")
            self.root.geometry("400x400")
            self.root.config(bg="#b2bec3")

            etiqueta = tk.Label(self.root, text="Piedra, Papel o Tijeras", font=("Arial", 18, "bold"), bg="#b2bec3")
            etiqueta.pack(pady=10)

            self.boton_piedra = tk.Button(self.root, text="Piedra", width=20, height=2, command=lambda: self.jugar("Piedra"))
            self.boton_piedra.pack(pady=5)

            self.boton_papel = tk.Button(self.root, text="Papel", width=20, height=2, command=lambda: self.jugar("Papel"))
            self.boton_papel.pack(pady=5)

            self.boton_tijeras = tk.Button(self.root, text="Tijeras", width=20, height=2, command=lambda: self.jugar("Tijeras"))
            self.boton_tijeras.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la interfaz de Piedra, Papel o Tijeras: {e}")

    def jugar(self, seleccion_usuario):
        try:
            opciones = ["Piedra", "Papel", "Tijeras"]
            seleccion_maquina = random.choice(opciones)

            if seleccion_usuario == seleccion_maquina:
                resultado = "Empate"
            elif (seleccion_usuario == "Piedra" and seleccion_maquina == "Tijeras") or \
                 (seleccion_usuario == "Papel" and seleccion_maquina == "Piedra") or \
                 (seleccion_usuario == "Tijeras" and seleccion_maquina == "Papel"):
                resultado = "¡Ganaste!"
            else:
                resultado = "¡Perdiste!"

            messagebox.showinfo("Resultado", f"Tú elegiste: {seleccion_usuario}\nLa máquina eligió: {seleccion_maquina}\n{resultado}")
            self.callback_fin_juego()
        except Exception as e:
            messagebox.showerror("Error", f"Error al jugar: {e}")



    def mostrar_resultado(self, eleccion_jugador, eleccion_computadora, resultado):
        mensaje = f"Tú elegiste: {eleccion_jugador}\nLa computadora eligió: {eleccion_computadora}\n\n{resultado}!"
        messagebox.showinfo("Resultado", mensaje)
        self.callback_fin_juego()

class Buscaminas:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.botones = {}
        self.minas = self.crear_minas(filas=8, columnas=8)
        self.crear_tablero(filas=8, columnas=8)

    def crear_tablero(self, filas, columnas):
        try:
            frame = tk.Frame(self.root)
            frame.pack(expand=True)
            for fila in range(filas):
                for columna in range(columnas):
                    boton = tk.Button(frame, width=3, height=1, command=lambda f=fila, c=columna: self.click(f, c))
                    boton.grid(row=fila, column=columna)
                    self.botones[(fila, columna)] = boton
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el tablero: {e}")

    def crear_minas(self, filas, columnas, num_minas=10):
        try:
            minas = set()
            while len(minas) < num_minas:
                mina = (random.randint(0, filas - 1), random.randint(0, columnas - 1))
                minas.add(mina)
            return minas
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear las minas: {e}")
            return set()

    def click(self, fila, columna):
        try:
            if (fila, columna) in self.minas:
                for (mf, mc) in self.minas:
                    self.botones[(mf, mc)].config(text="*", bg="red")
                messagebox.showinfo("Buscaminas", "¡Has perdido!")
                self.callback_fin_juego()
            else:
                self.revelar_zona_segura(fila, columna)
                if self.verificar_victoria():
                    messagebox.showinfo("Buscaminas", "¡Felicidades, has ganado!")
                    self.callback_fin_juego()
        except Exception as e:
            messagebox.showerror("Error", f"Error al hacer clic en la celda: {e}")

    def revelar_zona_segura(self, fila, columna):
        try:
            if (fila, columna) not in self.botones or self.botones[(fila, columna)]["text"] != "":
                return

            minas_adyacentes = self.contar_minas_adyacentes(fila, columna)
            self.botones[(fila, columna)].config(text=str(minas_adyacentes), state="disabled")

            if minas_adyacentes == 0:
                for f, c in self.obtener_celdas_adyacentes(fila, columna):
                    self.revelar_zona_segura(f, c)
        except Exception as e:
            messagebox.showerror("Error", f"Error al revelar zona segura: {e}")

    def contar_minas_adyacentes(self, fila, columna):
        try:
            return sum((f, c) in self.minas for f, c in self.obtener_celdas_adyacentes(fila, columna))
        except Exception as e:
            messagebox.showerror("Error", f"Error al contar las minas adyacentes: {e}")
            return 0

    def obtener_celdas_adyacentes(self, fila, columna):
        try:
            celdas = []
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if df == 0 and dc == 0:
                        continue
                    nf, nc = fila + df, columna + dc
                    if 0 <= nf < 8 and 0 <= nc < 8:
                        celdas.append((nf, nc))
            return celdas
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener celdas adyacentes: {e}")
            return []

    def verificar_victoria(self):
        try:
            return all(
                (fila, columna) in self.minas or self.botones[(fila, columna)]["state"] == "disabled"
                for fila in range(8) for columna in range(8)
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar la victoria: {e}")
            return False

