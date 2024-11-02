from flask import Flask, render_template, request, jsonify
import random

# Clase para el juego Triki
class Triki:
    def _init_(self):
        self.turn = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def mark_cell(self, i, j):
        if self.board[i][j] == "":
            self.board[i][j] = self.turn
            if self.check_winner():
                return f"¡{self.turn} ha ganado!"
            elif self.check_draw():
                return "¡Es un empate!"
            else:
                self.turn = "O" if self.turn == "X" else "X"
                return f"Turno de: {self.turn}"
        return "Celda ocupada."

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def reset_game(self):
        self.turn = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def display_board(self):
        for row in self.board:
            print(" | ".join(cell if cell else " " for cell in row))
            print("-" * 9)

# Clase para el juego Adivina el Número
class AdivinaNumero:
    def _init_(self):
        self.number_to_guess = random.randint(1, 100)
        self.guesses = 0

    def check_guess(self, guess):
        self.guesses += 1
        if guess < self.number_to_guess:
            return "Demasiado bajo!"
        elif guess > self.number_to_guess:
            return "Demasiado alto!"
        else:
            return f"¡Correcto! Adivinaste en {self.guesses} intentos."

# Clase para el juego Piedra, Papel o Tijeras
class PiedraPapelTijeras:
    def jugar(self, user_choice):
        choices = ["Piedra", "Papel", "Tijeras"]
        computer_choice = random.choice(choices)
        return self.determine_winner(user_choice, computer_choice), computer_choice

    def determine_winner(self, user, computer):
        if user == computer:
            return "Es un empate!"
        elif (user == "Piedra" and computer == "Tijeras") or \
                (user == "Papel" and computer == "Piedra") or \
                (user == "Tijeras" and computer == "Papel"):
            return "¡Ganaste!"
        else:
            return "¡La máquina gana!"

# Clase principal del menú de juegos
def main():
    print("Bienvenido al Casino de Juegos")
    user_name = input("Por favor, ingresa tu nombre: ")
    
    while True:
        print(f"\nHola, {user_name}! ¿Te gustaría jugar?")
        choice = input("Escribe 'sí' para jugar o 'no' para salir: ").strip().lower()
        
        if choice == 'no':
            print("¡Gracias por jugar!")
            break
        elif choice == 'sí':
            print("\nSelecciona un juego:")
            print("1. Triki")
            print("2. Adivina el Número")
            print("3. Piedra, Papel o Tijeras")
            print("4. Salir")
            game_choice = input("Selecciona un juego (1-4): ")
            
            if game_choice == '1':
                game = Triki()
                while True:
                    game.display_board()
                    row = int(input(f"Turno de {game.turn}. Elige la fila (0, 1, 2): "))
                    col = int(input(f"Elige la columna (0, 1, 2): "))
                    result = game.mark_cell(row, col)
                    if result:
                        game.display_board()
                        print(result)
                        break
            elif game_choice == '2':
                game = AdivinaNumero()
                while True:
                    guess = int(input("Adivina un número entre 1 y 100: "))
                    result = game.check_guess(guess)
                    print(result)
                    if "Correcto" in result:
                        break
            elif game_choice == '3':
                game = PiedraPapelTijeras()
                user_choice = input("Elige Piedra, Papel o Tijeras: ").capitalize()
                result, computer_choice = game.jugar(user_choice)
                print(f"Computadora eligió: {computer_choice}. {result}")
            elif game_choice == '4':
                print("¡Gracias por jugar!")
                break
            else:
                print("Opción inválida. Inténtalo de nuevo.")
        else:
            print("Opción inválida. Inténtalo de nuevo.")

if _name_ == "_main_":
    main()