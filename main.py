import sys
import time
import logic, misc

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
        self.matrice=logic.start(4)
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
        t=repr(tasta.char)
        if t in self.comenzi:
            self.matrice, done= self.comenzi[t](self.matrice,4)
            if done:
                self.matrice = logic.add_2(self.matrice,4)
                self.update_grid_cells()
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


j=joc()














