import sys
import time
import logic, misc
import numpy as np
import matplotlib.pyplot as plt

GAME_COLOR = "#a6bdbb"

EMPTY_COLOR = "#8eaba8"


AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"

NUMBER_OF_MOVES = 4
SAMPLE_COUNT = 50

from tkinter import Frame, Label, CENTER,Button
import random
highscore=0

class joc(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.bind("<Key>", self.tasta_apasata)
        self.comenzi = {"'w'": logic.up, "'s'" : logic.down, "'a'" : logic.left, "'d'" : logic.right}
        self.celule=[]
        self.score=0
        self.init_plansa()
        self.matrice=logic.start()
        self.draw_grid_cells()
        self.update_grid_cells()
        self.mainloop()

    def init_plansa(self):
        fundal =  Frame(self, bg=misc.BACKGROUND_COLOR_GAME, width=misc.SIZE, height=misc.SIZE)
        hi = Label(self, text="score:")
        hi.place(relx = 0.0,
                 rely = 1.0,
                 anchor ='sw')
        hi.grid(column=0, row=0)
        btn = Button(self, text="Play again", command=lambda: self.onclick())
        btn.place(relx = 0.0,
                  rely = 1.0,
                  anchor ='sw')
        fundal.grid()
        for i in range(4):
            linie=[]
            for j in range(4):
                cell = Frame(fundal, bg=misc.BACKGROUND_COLOR_CELL_EMPTY,
                             width=misc.SIZE / misc.GRID_LEN,
                             height=misc.SIZE / misc.GRID_LEN)
                cell.grid(row=i, column=j, padx=misc.GRID_PADDING,
                          pady=misc.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=misc.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=misc.FONT, width=5, height=2)
                t.grid()
                linie.append(t)
            self.celule.append(linie)
            self.score=hi

    def draw_grid_cells(self):
        for row in range(4):
            for col in range(4):
                tile_value = self.matrice[row][col]
                if not tile_value:
                    self.celule[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.celule[row][col].configure(text=str(
                        tile_value), bg=misc.TILE_COLORS[tile_value],
                        fg=misc.LABEL_COLORS[tile_value])
        self.update_idletasks()

    def update_grid_cells(self):
        total=0
        for i in range(4):
            for j in range(4):
                if self.matrice[i][j] == 0:
                    self.celule[i][j].configure(text="", bg=misc.BACKGROUND_COLOR_CELL_EMPTY)
                else:

                    self.celule[i][j].configure(text=str(self.matrice[i][j]), bg=misc.BACKGROUND_COLOR_DICT[self.matrice[i][j]],
                                                fg=misc.CELL_COLOR_DICT[self.matrice[i][j]])
                total+=self.matrice[i][j]
        self.score.configure(text="score: "+ str(total))


    def tasta_apasata(self, tasta):
        valid_game = True
        t=repr(tasta.char)
        if t in self.comenzi:
            self.matrice, done, score= self.comenzi[t](self.matrice,4)
            if done:
                self.matrice = logic.add_2(self.matrice,4)
                self.update_grid_cells()
                if logic.check_2048(self.matrice,4) == "WON":
                    self.celule[1][1].configure(text="You", bg="#9e948a")
                    self.celule[1][2].configure(text="won!", bg="#9e948a")
                if logic.check_continue(self.matrice,4) =="LOST":
                    self.celule[1][1].configure(text="You", bg="#9e948a")
                    self.celule[1][2].configure(text="lost!", bg="#9e948a")
        if t == AI_PLAY_KEY:
            move_count = 0
            while valid_game:
                self.matrice, valid_game = ai_move(self.matrice, 40, 30)
                if valid_game:
                    self.matrice = logic.add_new_tile(self.matrice)
                    self.draw_grid_cells()
                move_count += 1
                total = 0

                for i in range(len(self.matrice)):
                    for j in range(len(self.matrice[i])):
                        total += self.matrice[i][j]
                total += 2
                self.score.configure(text="score: "+ str(total))
            if logic.check_2048(self.matrice,4) == "WON":
                self.celule[3][1].configure(text="You", bg="#9e948a")
                self.celule[3][2].configure(text="won!", bg="#9e948a")
            if logic.check_continue(self.matrice,4) =="LOST":
                self.celule[3][1].configure(text="You", bg="#9e948a")
                self.celule[3][2].configure(text="lost!", bg="#9e948a")
        if t == AI_KEY:
            self.matrice, move_made = ai_move(self.matrice, 20, 30)
            if move_made:
                self.matrice = logic.add_new_tile(self.matrice)
                self.draw_grid_cells()
                move_made = False
            if logic.check_2048(self.matrice,4) == "WON":
                self.celule[1][1].configure(text="You", bg="#9e948a")
                self.celule[1][2].configure(text="won!", bg="#9e948a")
            if logic.check_continue(self.matrice,4) =="LOST":
                self.celule[1][1].configure(text="You", bg="#9e948a")
                self.celule[1][2].configure(text="lost!", bg="#9e948a")
    def onclick(self):
        global highscore

        self.destroy()
        g=joc()


def ai_move(board, searches_per_move, search_length):
    first_moves = [logic.down, logic.left, logic.right, logic.up]
    scores = np.zeros(4)

    for first_index in range(4):
        first_move = first_moves[first_index]
        first_board, first_valid, first_score = first_move(board,4)

        if first_valid:
            first_board = logic.add_new_tile(first_board)
            scores[first_index] += first_score
        else:
            continue

        for later_moves in range(searches_per_move):
            move_number = 1
            search_board = np.copy(first_board)
            is_valid = True

            while is_valid and move_number < search_length:
                search_board, is_valid, score = logic.random_move(search_board,4)
                print(score)
                if is_valid:
                    search_board = logic.add_new_tile(search_board)
                    scores[first_index] += score
                    move_number += 1

    best_move_index = np.argmax(scores)
    best_move = first_moves[best_move_index]
    final_board, postition_valid, _ = best_move(board,4)

    return final_board, postition_valid

# test_matrix = logic.start(4)
# test_matrix, position_valid = ai_move(test_matrix, 10, 1000)
# print(test_matrix)
# def newgame(matrix, position_valid):
#     if logic.check_2048(matrix, 4) == "WON":
#         print("WON")
#         return matrix
#     print(matrix)
#     test_matrix, position_valid1 = ai_move(matrix, 5, 5)
#     newgame(test_matrix,position_valid1)


def ai_play(board):
    move_number = 0
    valid_game = True
    while valid_game:
        move_number += 1
        number_of_simulations, search_length = logic.get_search_params(move_number)
        board, valid_game = ai_move(board, number_of_simulations, search_length)
        if valid_game:
            board = logic.add_2(board,4)
        if logic.check_2048(board,4):
            valid_game = False
        print(board)
        print(move_number)
    print(board)
    return np.amax(board)

def ai_plot(move_func):
    tick_locations = np.arange(1, 12)
    final_scores = []
    for _ in range(SAMPLE_COUNT):
        print('thing is ', _)
        board = logic.start()
        game_is_win = ai_play(board)
        final_scores.append(game_is_win)
    all_counts = np.zeros(11)
    unique, counts = np.unique(np.array(final_scores), return_counts=True)
    unique = np.log2(unique).astype(int)
    index = 0

    for tick in tick_locations:
        if tick in unique:
            all_counts[tick-1] = counts[index]
            index += 1

    plt.bar(tick_locations, all_counts)
    plt.xticks(tick_locations, np.power(2, tick_locations))
    plt.xlabel("Score of Game", fontsize = 24)
    plt.ylabel(f"Frequency per {SAMPLE_COUNT} runs", fontsize = 24)
    plt.show()

j=joc()














