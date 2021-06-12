import random, misc
import numpy as np

NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2 ,2, 4])
SPM_SCALE_PARAM = 10
SL_SCALE_PARAM = 4
SEARCH_PARAM = 200
CELL_COUNT = 4
NUMBER_OF_SQUARES = CELL_COUNT * CELL_COUNT

def start():

    # Initializam o matrice de nr_lines x nr_lines cu zerouri, vom folosi matricea pe post de tabla de joc
    board = np.zeros((NUMBER_OF_SQUARES), dtype="int")
    initial_twos = np.random.default_rng().choice(NUMBER_OF_SQUARES, 1, replace=False)
    board[initial_twos] = 2
    board = board.reshape((CELL_COUNT, CELL_COUNT))


    # Prezentam utilizatorului controalele jocului
    print("Game controls:")
    print("'W' , 'w' or Up Arrow : Move Up")
    print("'A' , 'a' or Left Arrow : Move Left")
    print("'S' , 's' or Down Arrow : Move Down")
    print("'D' , 'd' or Right Arrow : Move Right")
    print("'P' or 'p' : Let the AI play")
    print("'Q' or 'q' : Make one move with the AI")

    # Cand vom incepe jocul il incepem cu un singur 2 pe masa, deci
    # adaugam un nou bloc de 2 dupa fiecare mutare a utilizatorului
    #add_2(matrix, nr_lines)


    return board

def add_2(matrix, nr_lines):

    # Alegem un punct random in matricea noastra
    row = random.randint(0, nr_lines-1)
    column = random.randint(0, nr_lines-1)

    # Cat timp punctul nostru este diferit de 0 (este ocupat de alta casuta), schimbam punctul pana ajungem la unul nul
    while matrix[row][column] != 0:
        row = random.randint(0, nr_lines-1)
        column = random.randint(0, nr_lines-1)

    # Punem 2 in blocul gasit liber
    matrix[row][column] = 2
    return matrix

# Verificam daca exita un bloc de 2048, in cazul in care exista jocul este castigat
def check_2048(matrix, nr_lines):
    for i in range(nr_lines):
        for j in range(nr_lines):
            if(matrix[i][j] == 2048):
                return "WON"

# Verificam daca jocul poate fi continuat
def check_continue(matrix, nr_lines):

    # Daca avem cel putin un bloc 0, jocul poate fi continuat
    for i in range(nr_lines):
        for j in range(nr_lines):
            if(matrix[i][j]== 0):
                return 'GAME NOT OVER'

    # Daca toate blocurile sunt ocupate dar mai putem face o mutare, jocul poate fi continuat
    for i in range(nr_lines - 1):
        for j in range(nr_lines - 1):
            if(matrix[i][j]== matrix[i + 1][j] or matrix[i][j]== matrix[i][j + 1]):
                return 'GAME NOT OVER'

    for j in range(nr_lines - 1):
        if(matrix[3][j]== matrix[3][j + 1]):
            return 'GAME NOT OVER'

    for i in range(nr_lines - 1):
        if(matrix[i][3]== matrix[i + 1][3]):
            return 'GAME NOT OVER'

    # In cazul in care nu putem face niciuna dintre mutarile de mai sus, jocul nu poate fi continuat, am pierdut
    return 'LOST'

# Functie pentru a comprima matricea inainte si dupa merge, vom alege ca acest compress sa fie la stanga
def compress(matrix, nr_lines):

    # Variabila de tip bool sa urmarim daca s-au facut schimbari

    done = False

    # Noua matrice
    new = []
    for i in range(nr_lines):
        new.append([0] * nr_lines)



    for i in range(nr_lines):
        position = 0
        for j in range(nr_lines):
            if matrix[i][j] != 0:

                # Daca blocul nu este liber vom shifta numarul in locul anterior
                # de pe acel rand, determinat de variabila position
                new[i][position] = matrix[i][j]

                if j != position:
                    done = True
                position += 1

    return new, done

# Functie pentru a combina blocurile dupa ce comprimam matricea
def merge(matrix, nr_lines, done):
    for i in range(nr_lines):
        for j in range(nr_lines-1):
            if matrix[i][j] == matrix[i][j+1] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i][j+1] = 0
                done = True
    return matrix, done


# Abordarea noastra este comprimare -> combinare -> comprimare
# Ne vom folosi de functiile transpose si reverse pentru a manevra mai usor matricea
# din moment ce avand o shiftare facuta, folosind transpose si reverse putem face cam
# orice shiftare dorim (sus, jos, stanga, dreapta)

def reverse(matrix):
    new = []
    for i in range(len(matrix)):
        new.append([])
        for j in range(len(matrix[0])):
            new[i].append(matrix[i][len(matrix[0])-j-1])
    return new

def transpose(matrix):
    new = []
    for i in range(len(matrix[0])):
        new.append([])
        for j in range(len(matrix)):
            new[i].append(matrix[j][i])
    return new


# Acum functiile pentru modificarea matricei pentru mutarile sus/jos/stanga/dreapta

def up(matrix, nr_lines):
    print("UP")

    matrix = transpose(matrix)

    matrix, done = compress(matrix,nr_lines)
    matrix, done = merge(matrix,nr_lines, done)
    matrix = compress(matrix,nr_lines)[0]

    matrix = transpose(matrix)

    score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            score += matrix[i][j]

    score += 2
    return matrix, done, score


def down(matrix, nr_lines):
    print("DOWN")

    matrix = reverse(transpose(matrix))

    matrix, done = compress(matrix,nr_lines)
    matrix, done = merge(matrix,nr_lines, done)
    matrix = compress(matrix,nr_lines)[0]

    matrix = transpose(reverse(matrix))

    score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            score += matrix[i][j]

    score += 2

    return matrix, done, score


# Pentru ca am facut compress-ul la stanga, nu avem nevoie de reverse si nici de transpose pentru shiftare
def left(matrix, nr_lines):
    print("LEFT")

    matrix, done = compress(matrix,nr_lines)
    matrix, done = merge(matrix,nr_lines, done)
    matrix = compress(matrix,nr_lines)[0]

    score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            score += matrix[i][j]

    score += 2

    return matrix, done, score


def right(matrix, nr_lines):
    print("RIGHT")
    matrix = reverse(matrix)
    matrix, done = compress(matrix,nr_lines)
    matrix, done = merge(matrix,nr_lines, done)
    matrix = compress(matrix,nr_lines)[0]
    matrix = reverse(matrix)

    score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            score += matrix[i][j]

    score += 2
    return matrix, done, score


def random_move(matrix, nr_lines):
    i = random.randint(0,3)
    if i == 0:
        return right(matrix, nr_lines)
    elif i == 1:
        return left(matrix, nr_lines)
    elif i == 2:
        return up(matrix, nr_lines)
    elif i == 3:
        return down(matrix, nr_lines)


def add_new_tile(board):
    tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(0, len(NEW_TILE_DISTRIBUTION))]
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
    tile_loc = np.random.randint(0, len(tile_row_options))
    board[tile_row_options[tile_loc]][tile_col_options[tile_loc]] = tile_value
    return board


def get_search_params(move_number):
    searches_per_move = SPM_SCALE_PARAM * (1+(move_number // SEARCH_PARAM))
    search_length = SL_SCALE_PARAM * (1+(move_number // SEARCH_PARAM))
    return searches_per_move, search_length