import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Triki:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.turn = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.vs_computer = messagebox.askyesno("Triki", "¿Quieres jugar contra la computadora?")
        self.create_board()

    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        for i in range(9):
            button = tk.Button(frame, text='', font=('Arial', 20), width=5, height=2,
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def on_click(self, index):
        if self.board[index] == '':
            self.board[index] = self.turn
            self.buttons[index].config(text=self.turn)
            if self.check_winner():
                messagebox.showinfo("Triki", f"¡El jugador {self.turn} ha ganado!")
                self.callback_fin_juego()
            elif '' not in self.board:
                messagebox.showinfo("Triki", "¡Es un empate!")
                self.callback_fin_juego()
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                if self.vs_computer and self.turn == 'O':
                    self.computer_move()

    def computer_move(self):
        empty_indices = [i for i, val in enumerate(self.board) if val == '']
        index = random.choice(empty_indices)
        self.on_click(index)

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                return True
        return False


class Serpiente:
    def __init__(self, root, callback_fin_juego):
        self.root = root
        self.callback_fin_juego = callback_fin_juego
        self.canvas = tk.Canvas(self.root, bg="black", width=500, height=500)  # Valores por defecto
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Posición inicial de la serpiente
        self.snake = [(250, 250), (240, 250), (230, 250)]
        self.direction = 'Right'
        self.food = None  # Inicializamos sin posición
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
        # Definimos la posición de la comida asegurándonos de que esté dentro de los límites actuales
        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 0 else 500
        height = self.canvas.winfo_height() if self.canvas.winfo_height() > 0 else 500
        x = random.randint(0, (width // 10) - 1) * 10
        y = random.randint(0, (height // 10) - 1) * 10
        self.food = (x, y)

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
        self.options = ["Piedra", "Papel", "Tijeras"]
        self.vs_computer = messagebox.askyesno("Piedra, Papel o Tijeras", "¿Quieres jugar contra la computadora?")
        self.play_game()

    def play_game(self):
        player_choice = simpledialog.askstring("Piedra, Papel o Tijeras", "Elige: Piedra, Papel o Tijeras")
        if player_choice is None:
            return
        if self.vs_computer:
            computer_choice = random.choice(self.options)
            self.determine_winner(player_choice, computer_choice)
        else:
            opponent_choice = simpledialog.askstring("Piedra, Papel o Tijeras", "Jugador 2: Elige Piedra, Papel o Tijeras")
            if opponent_choice:
                self.determine_winner(player_choice, opponent_choice)

    def determine_winner(self, player, opponent):
        if player == opponent:
            result = "Empate"
        elif (player == "Piedra" and opponent == "Tijeras") or \
                (player == "Papel" and opponent == "Piedra") or \
                (player == "Tijeras" and opponent == "Papel"):
            result = "Ganaste"
        else:
            result = "Perdiste"
        messagebox.showinfo("Resultado", f"El oponente eligió {opponent}. {result}.")
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
