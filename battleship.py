from tkinter import *
from random import randint

class Battleship:
    def __init__(self, master):
        self.master = master
        master.title("Battleship")

        # Initialize player names and scores
        self.player_1_name = "Player 1"
        self.player_2_name = "Player 2"
        self.player_1_score = 0
        self.player_2_score = 0

        # Create labels for player names and scores
        self.player_1_label = Label(master, text=f"{self.player_1_name}'s Score: {self.player_1_score}")
        self.player_1_label.grid(row=0, column=0, columnspan=6)
        self.player_2_label = Label(master, text=f"{self.player_2_name}'s Score: {self.player_2_score}")
        self.player_2_label.grid(row=0, column=12, columnspan=6)

        # Create a timer interval (in milliseconds) for the animation
        self.animation_interval = 500  # Adjust as needed

        # Initialize the game board for both players
        self.player_1_board = [[0 for x in range(10)] for y in range(10)]
        self.player_2_board = [[0 for x in range(10)] for y in range(10)]

        # Create the grid of buttons for player 1's board
        self.player_1_buttons = []
        for i in range(10):
            row = []
            for j in range(10):
                button = Button(master, text="", width=2, height=1, command=lambda x=i, y=j: self.fire(x, y, player=1))
                button.grid(row=i + 2, column=j)
                row.append(button)
            self.player_1_buttons.append(row)

        # Create the grid of buttons for player 2's board
        self.player_2_buttons = []
        for i in range(10):
            row = []
            for j in range(10):
                button = Button(master, text="", width=2, height=1, command=lambda x=i, y=j: self.fire(x, y, player=2))
                button.grid(row=i + 2, column=j + 12)  # Adjust the column position for player 2
                row.append(button)
            self.player_2_buttons.append(row)

        # Initialize the ships for both players
        self.ships = [(1, 5), (2, 4), (3, 3), (4, 2)]

        # Randomly place the ships on both boards
        self.place_ships(self.player_1_board)
        self.place_ships(self.player_2_board)

        # Initialize the remaining number of ships for both players
        self.remaining_1 = len(self.ships)
        self.remaining_2 = len(self.ships)

        # Create a label to display game messages
        self.message_label = Label(master, text=f"{self.player_1_name}'s turn")
        self.message_label.grid(row=12, columnspan=10)

        # Initialize the current player
        self.current_player = 1

    def place_ships(self, board):
        for size, count in self.ships:
            for i in range(count):
                placed = False
                while not placed:
                    x = randint(0, 9)
                    y = randint(0, 9)
                    horizontal = randint(0, 1) == 0
                    if self.check_loc(board, x, y, size, horizontal):
                        self.ship_loc(board, x, y, size, horizontal)
                        placed = True

    def check_loc(self, board, x, y, size, horizontal):
        if horizontal:
            if y + size > 10:
                return False
            for j in range(y, y + size):
                if board[x][j] != 0:
                    return False
        else:
            if x + size > 10:
                return False
            for i in range(x, x + size):
                if board[i][y] != 0:
                    return False
        return True

    def ship_loc(self, board, x, y, size, horizontal):
        for i in range(size):
            if horizontal:
                board[x][y + i] = size
            else:
                board[x + i][y] = size

    def fire(self, x, y, player):
        if player == 1:
            board = self.player_2_board
            buttons = self.player_2_buttons
            remaining = self.remaining_2
            opponent = 2
            player_name = self.player_1_name
        else:
            board = self.player_1_board
            buttons = self.player_1_buttons
            remaining = self.remaining_1
            opponent = 1
            player_name = self.player_2_name

        if board[x][y] == 0:
            buttons[x][y].config(bg="gray", text="X")
            self.message_label.config(text=f"{player_name}'s turn")
        elif board[x][y] == -1:
            pass
        else:
            size = board[x][y]
            self.animate_sinking_ship(x, y, size, buttons)  # Animate the ship sinking
            self.master.after(self.animation_interval, lambda: self.sink_ship(x, y, size, buttons, board, remaining, player, player_name, opponent))

    def animate_sinking_ship(self, x, y, size, buttons):
        for i in range(size):
            buttons[x][y + i].config(bg="orange")  # Change color to create the animation effect
        self.master.update()  # Update the GUI to show the color change

    def sink_ship(self, x, y, size, buttons, board, remaining, player, player_name, opponent):
        for i in range(size):
            buttons[x][y + i].config(bg="red", text=str(size))
            board[x][y + i] = -1
        remaining -= 1
        if remaining == 0:
            self.message_label.config(text=f"{player_name} WINS!!!")
            if player == 1:
                self.player_1_score += 1
            else:
                self.player_2_score += 1
            self.update_scores()
            self.disable_buttons()
        else:
            self.current_player = opponent
            self.message_label.config(text=f"{self.get_player_name(self.current_player)}'s turn")

    def get_player_name(self, player):
        return self.player_1_name if player == 1 else self.player_2_name

    def update_scores(self):
        self.player_1_label.config(text=f"{self.player_1_name}'s Score: {self.player_1_score}")
        self.player_2_label.config(text=f"{self.player_2_name}'s Score: {self.player_2_score}")

    def disable_buttons(self):
        for i in range(10):
            for j in range(10):
                self.player_1_buttons[i][j].config(state=DISABLED)
                self.player_2_buttons[i][j].config(state=DISABLED)

root = Tk()
game = Battleship(root)
root.mainloop()
