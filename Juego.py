import tkinter as tk
from tkinter import messagebox, simpledialog
import random



class Triki:
    def __init__(self, root):
        self.root = root
        self.turn = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []

        self.create_board()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text='', font=('Arial', 20), width=5, height=2,
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def on_click(self, index):
        if self.board[index] == '':
            self.board[index] = self.turn
            self.buttons[index].config(text=self.turn)
            if self.check_winner():
                messagebox.showinfo("Triki", f"¡El jugador {self.turn} ha ganado!")
                self.reset_game()
            elif '' not in self.board:
                messagebox.showinfo("Triki", "¡Es un empate!")
                self.reset_game()
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                return True
        return False

    def reset_game(self):
        self.turn = 'X'
        self.board = ['' for _ in range(9)]
        for button in self.buttons:
            button.config(text='')


class Serpiente:
    def __init__(self, root):
        self.root = root
        # Ampliación del tamaño de la cuadrícula a 500x500 píxeles
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="black")
        self.canvas.pack()

        # Inicialización de la serpiente
        self.snake = [(250, 250), (240, 250), (230, 250)]
        self.direction = 'Right'

        # Posición inicial de la comida
        self.food = self.create_food()

        self.move_snake()
        self.root.bind("<KeyPress>", self.change_direction)

    def create_food(self):
        # Aseguramos que la comida esté en la cuadrícula de 10 píxeles en 500x500
        x = random.randint(0, 49) * 10
        y = random.randint(0, 49) * 10
        return (x, y)

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

        if new_head == self.food:
            self.food = self.create_food()
        else:
            self.snake.pop()  # Quitar el último segmento de la serpiente

        if (head_x < 0 or head_x >= 500 or head_y < 0 or head_y >= 500 or new_head in self.snake):
            messagebox.showinfo("Serpiente", "¡Perdiste!")
            self.root.quit()
            return

        self.snake.insert(0, new_head)
        self.update_canvas()
        self.root.after(100, self.move_snake)

    def update_canvas(self):
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green")
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red")


class AdivinaNumero:
    def __init__(self, root):
        self.root = root
        self.target_number = random.randint(1, 100)
        self.prompt_guess()

    def prompt_guess(self):
        guess = simpledialog.askinteger("Adivina el Número", "Adivina un número entre 1 y 100:")
        if guess is not None:
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


class PiedraPapelTijeras:
    def __init__(self, root):
        self.root = root
        self.options = ["Piedra", "Papel", "Tijeras"]
        self.play_game()

    def play_game(self):
        player_choice = simpledialog.askstring("Piedra, Papel o Tijeras", "Elige: Piedra, Papel o Tijeras")
        if player_choice is None:
            return
        computer_choice = random.choice(self.options)
        self.determine_winner(player_choice, computer_choice)

    def determine_winner(self, player, computer):
        if player == computer:
            result = "Empate"
        elif (player == "Piedra" and computer == "Tijeras") or \
                (player == "Papel" and computer == "Piedra") or \
                (player == "Tijeras" and computer == "Papel"):
            result = "¡Ganaste!"
        else:
            result = "Perdiste"

        messagebox.showinfo("Resultado", f"Tú elegiste {player}, la computadora eligió {computer}. {result}")


class Buscaminas:
    def __init__(self, root):
        self.root = root
        self.buttons = {}
        # Ampliación de la cuadrícula a 8x8 para más tamaño de juego
        self.mines = self.create_mines(rows=8, cols=8)

        self.create_board(rows=8, cols=8)

    def create_board(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                button = tk.Button(self.root, width=3, height=1, command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                self.buttons[(row, col)] = button

    def create_mines(self, rows, cols):
        return {(random.randint(0, rows - 1), random.randint(0, cols - 1)) for _ in range(10)}

    def click(self, row, col):
        if (row, col) in self.mines:
            messagebox.showinfo("Buscaminas", "¡Has perdido!")
            self.root.quit()
        else:
            self.buttons[(row, col)].config(text="0", state="disabled")
