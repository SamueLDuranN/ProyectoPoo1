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
        for i in range(3):
            for j in range(3):
                boton = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=5,
                    height=2,
                    bg="#dfe6e9",  # Color de fondo
                    fg="#2d3436",  # Color de texto
                    activebackground="#b2bec3",  # Fondo cuando se presiona
                    relief="groove",
                    bd=3,
                    command=lambda i=i, j=j: self.marcar_casilla(i, j)
                )
                boton.grid(row=i, column=j, padx=5, pady=5)
                self.tablero[i][j] = boton

    def marcar_casilla(self, i, j):
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

    def verificar_ganador(self):
        # Comprobar filas, columnas y diagonales
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


class Serpiente:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.canvas = tk.Canvas(self.root, bg="black", width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Posición inicial de la serpiente
        self.snake = [(250, 250), (240, 250), (230, 250)]
        self.direction = 'Right'
        self.food = None
        self.root.update()  # Actualizamos la ventana para obtener el tamaño del canvas
        self.place_food()  # Colocamos la comida cuando el canvas esté configurado

        self.move_snake()
        self.root.bind("<KeyPress>", self.change_direction)
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Actualizamos el tamaño del canvas y colocamos la comida nuevamente si es necesario
        self.canvas.config(width=event.width, height=event.height)
        if self.food is None or not (0 <= self.food[0] < event.width and 0 <= self.food[1] < event.height):
            self.place_food()

    def place_food(self):
        # Intentamos obtener el ancho y alto del canvas y colocar la comida solo si los valores son válidos
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width > 0 and height > 0:
            x = random.randint(0, (width // 10) - 1) * 10
            y = random.randint(0, (height // 10) - 1) * 10
            self.food = (x, y)
        else:
            # Volvemos a llamar a place_food después de un pequeño retraso si el tamaño aún no está listo
            self.root.after(100, self.place_food)

    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = {'Left', 'Right', 'Up', 'Down'}
        opposite_directions = {('Left', 'Right'), ('Right', 'Left'), ('Up', 'Down'), ('Down', 'Up')}

        if new_direction in all_directions and (self.direction, new_direction) not in opposite_directions:
            self.direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == 'Left':
            head_x -= 10
        elif self.direction == 'Right':
            head_x += 10
        elif self.direction == 'Up':
            head_y -= 10
        elif self.direction == 'Down':
            head_y += 10

        new_head = (head_x, head_y)

        # Comprobamos colisión con comida
        if new_head == self.food:
            self.place_food()
        else:
            self.snake.pop()

        # Comprobamos colisión con el borde o consigo misma
        if (head_x < 0 or head_x >= self.canvas.winfo_width() or
                head_y < 0 or head_y >= self.canvas.winfo_height() or new_head in self.snake):
            messagebox.showinfo("Serpiente", "¡Perdiste!")
            self.callback_fin_juego()
            return

        # Agregamos nueva posición de la cabeza y actualizamos el canvas
        self.snake.insert(0, new_head)
        self.update_canvas()
        self.root.after(100, self.move_snake)

    def update_canvas(self):
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green")
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")



class AdivinaNumero:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.target_number = random.randint(1, 100)
        self.prompt_guess()

    def prompt_guess(self):
        guess = simpledialog.askinteger("Adivina el Número", "Adivina un número entre 1 y 100:")
        if guess is None:  # Si el usuario presiona "Cancel"
            self.callback_fin_juego()  # Regresa al menú principal
        else:
            self.check_guess(guess)

    def check_guess(self, guess):
        if guess < self.target_number:
            messagebox.showinfo("Resultado", "Demasiado bajo. ¡Inténtalo de nuevo!")
            self.prompt_guess()
        elif guess > self.target_number:
            messagebox.showinfo("Resultado", "Demasiado alto. ¡Inténtalo de nuevo!")
            self.prompt_guess()
        else:
            messagebox.showinfo("Resultado", "¡Felicidades! Adivinaste el número.")
            self.callback_fin_juego()

class PiedraPapelTijeras:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.crear_interfaz_piedra_papel_tijeras()

    def crear_interfaz_piedra_papel_tijeras(self):
        self.root.title("Piedra, Papel o Tijeras")
        self.root.geometry("400x400")
        self.root.config(bg="#b2bec3")

        label = tk.Label(self.root, text="Piedra, Papel o Tijeras", font=("Arial", 18, "bold"), bg="#b2bec3", fg="#2d3436")
        label.pack(pady=20)

        self.boton_piedra = self.crear_boton("Piedra", "#e74c3c", self.jugar_piedra)
        self.boton_piedra.pack(pady=10)

        self.boton_papel = self.crear_boton("Papel", "#3498db", self.jugar_papel)
        self.boton_papel.pack(pady=10)

        self.boton_tijeras = self.crear_boton("Tijeras", "#2ecc71", self.jugar_tijeras)
        self.boton_tijeras.pack(pady=10)

    def crear_boton(self, texto, color, comando):
        return tk.Button(
            self.root,
            text=texto,
            font=("Arial", 14, "bold"),
            width=15,
            height=2,
            bg=color,
            fg="white",
            activebackground="#95a5a6",
            relief="raised",
            bd=4,
            command=comando
        )

    def jugar_piedra(self):
        self.jugar("Piedra")

    def jugar_papel(self):
        self.jugar("Papel")

    def jugar_tijeras(self):
        self.jugar("Tijeras")

    def jugar(self, eleccion_jugador):
        opciones = ["Piedra", "Papel", "Tijeras"]
        eleccion_computadora = random.choice(opciones)

        resultado = self.determine_winner(eleccion_jugador, eleccion_computadora)
        self.mostrar_resultado(eleccion_jugador, eleccion_computadora, resultado)

    def determine_winner(self, eleccion_jugador, eleccion_computadora):
        if eleccion_jugador == eleccion_computadora:
            return "Empate"
        elif (eleccion_jugador == "Piedra" and eleccion_computadora == "Tijeras") or \
             (eleccion_jugador == "Papel" and eleccion_computadora == "Piedra") or \
             (eleccion_jugador == "Tijeras" and eleccion_computadora == "Papel"):
            return "Ganaste"
        else:
            return "Perdiste"

    def mostrar_resultado(self, eleccion_jugador, eleccion_computadora, resultado):
        mensaje = f"Tú elegiste: {eleccion_jugador}\nLa computadora eligió: {eleccion_computadora}\n\n{resultado}!"
        messagebox.showinfo("Resultado", mensaje)
        self.callback_fin_juego()



class Buscaminas:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.buttons = {}
        self.mines = self.create_mines(rows=8, cols=8)
        self.create_board(rows=8, cols=8)

    def create_board(self, rows, cols):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        for row in range(rows):
            for col in range(cols):
                button = tk.Button(frame, width=3, height=1, command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

    def create_mines(self, rows, cols, num_mines=10):
        mines = set()
        while len(mines) < num_mines:
            mine = (random.randint(0, rows - 1), random.randint(0, cols - 1))
            mines.add(mine)
        return mines

    def click(self, row, col):
        if (row, col) in self.mines:
            for (mr, mc) in self.mines:
                self.buttons[(mr, mc)].config(text="*", bg="red")
            messagebox.showinfo("Buscaminas", "¡Has perdido!")
            self.callback_fin_juego()
        else:
            self.reveal_safe_zone(row, col)
            if self.check_victory():
                messagebox.showinfo("Buscaminas", "¡Felicidades, has ganado!")
                self.callback_fin_juego()

    def reveal_safe_zone(self, row, col):
        if (row, col) not in self.buttons or self.buttons[(row, col)]["text"] != "":
            return

        adjacent_mines = self.count_adjacent_mines(row, col)
        self.buttons[(row, col)].config(text=str(adjacent_mines), state="disabled")

        if adjacent_mines == 0:
            for r, c in self.get_adjacent_cells(row, col):
                self.reveal_safe_zone(r, c)

    def count_adjacent_mines(self, row, col):
        return sum((r, c) in self.mines for r, c in self.get_adjacent_cells(row, col))

    def get_adjacent_cells(self, row, col):
        cells = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    cells.append((nr, nc))
        return cells

    def check_victory(self):
        return all(
            (row, col) in self.mines or self.buttons[(row, col)]["state"] == "disabled"
            for row in range(8) for col in range(8)
        )
