import tkinter as tk
from tkinter import messagebox

# Definición de la clase Triki basada en la lógica del archivo
class Triki:
    def __init__(self):
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
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset(self):
        self.__init__()


# Creación de la interfaz gráfica con tkinter
class TrikiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Triki (Tic-Tac-Toe)")
        self.game = Triki()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 20), width=5, height=2,
                                command=lambda i=i, j=j: self.mark_cell(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3)

    def mark_cell(self, i, j):
        result = self.game.mark_cell(i, j)
        self.buttons[i][j].config(text=self.game.board[i][j])

        if "ganado" in result or "empate" in result:
            messagebox.showinfo("Resultado", result)
            self.reset_game()
        elif result == "Celda ocupada.":
            messagebox.showwarning("Advertencia", "Esta celda ya está ocupada.")
        else:
            self.root.title(result)

    def reset_game(self):
        self.game.reset()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.root.title("Juego de Triki (Tic-Tac-Toe)")

# Crear y ejecutar la aplicación
root = tk.Tk()
app = TrikiApp(root)
root.mainloop()
