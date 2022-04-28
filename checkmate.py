#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Checkmate
"""

import pygame
import random
import time
import os
import sys
import datetime

os.environ['SDL_VIDEO_CENTERED'] = '1'

from pygame.locals import *

square = 70
xplus = 50
yplus = 30

fig = [[None for i in range(3)] for j in range(6)]

for j in range(1,3):
    filename = 'K' + str(j) + '.png'
    fig[0][j-1] = pygame.image.load(filename)
    filename = 'Q' + str(j) + '.png'
    fig[1][j-1] = pygame.image.load(filename)
    filename = 'R' + str(j) + '.png'
    fig[2][j-1] = pygame.image.load(filename)
    filename = 'B' + str(j) + '.png'
    fig[3][j-1] = pygame.image.load(filename)
    filename = 'N' + str(j) + '.png'
    fig[4][j-1] = pygame.image.load(filename)
    filename = 'P' + str(j) + '.png'
    fig[5][j-1] = pygame.image.load(filename)

select = pygame.image.load("select.png")
target = pygame.image.load("target.png")

b = [[0 for i in range(8)] for j in range(8)]

# White figures:
b[0][0] = 3
b[1][0] = 5
b[2][0] = 4
b[3][0] = 2
b[4][0] = 1
b[7][0] = 3
b[6][0] = 5
b[5][0] = 4

for i in range(8):
    b[i][1] = 6

# Black figures:
b[0][7] = 13
b[1][7] = 15
b[2][7] = 14
b[3][7] = 12
b[4][7] = 11
b[7][7] = 13
b[6][7] = 15
b[5][7] = 14

for i in range(8):
    b[i][6] = 16

board_value = 0

width = square * 8 + 2 * xplus
height = square * 8 + 2 * yplus

screen = pygame.display.set_mode((width, height))

def draw_figure(column, row, which):
    if which == 1:
        f = fig[0][0]
    if which == 2:
        f = fig[1][0]
    if which == 3:
        f = fig[2][0]
    if which == 4:
        f = fig[3][0]
    if which == 5:
        f = fig[4][0]
    if which == 6:
        f = fig[5][0]
    if which == 11:
        f = fig[0][1]
    if which == 12:
        f = fig[1][1]
    if which == 13:
        f = fig[2][1]
    if which == 14:
        f = fig[3][1]
    if which == 15:
        f = fig[4][1]
    if which == 16:
        f = fig[5][1]

    if which == 20:
        f = select
    if which == 21:
        f = target

    if which != 0:
        sizex = f.get_rect().w
        sizey = f.get_rect().h
        correctionx = (square-sizex)/2
        correctiony = (square-sizey)/2
        screen.blit(f,(int(column*square+correctionx+xplus),int((7-row)*square+correctiony+yplus)))

def draw_board():
    board_color = (0,128,0,255)
    pygame.draw.rect(screen, board_color, (0,0,width,height), 0)

    for i in range(8):
        for j in range(8):
            if ((i+j) % 2) == 0:
                field_color = (128,128,128,255)
            else:
                field_color = (192,192,192,255)
            pygame.draw.rect(screen, field_color, (i*square+xplus,(7-j)*square+yplus,square,square), 0)
            draw_figure(i, j, b[i][j])

    if pygame.font:
        size = 30
        white = (250, 250, 250)
        font = pygame.font.Font(None, size)
        for i in range(8):
            text = font.render(str(i+1), 1, white)
            screen.blit(text, (30, height-i*square-80))
        for i in range(8):
            text = font.render(str(chr(i+ord('a'))), 1, white)
            screen.blit(text, (i*square+xplus+30,height-25))


running = True

pygame.key.set_repeat(500, 30)

clock = pygame.time.Clock()
clock.tick()

pygame.init()
draw_board()


def empty(column, row):
    return b[int(column)][int(row)] == 0

def black(column, row):
    return b[int(column)][int(row)] >= 10

def white(column, row):
    ez = b[int(column)][int(row)]
    return ez >= 1 and ez <= 6

def opposite(column, row, p):
    if p == 0: # search for White's opposite's figures
        return black(column, row)
    return white(column, row)

def same(column, row, p):
    if p == 0: # search for White's figures
        return white(column, row)
    return black(column, row)

def to_move_possible(column, row):
    """Return the possible moves of a player, eventually positions in check are also possible."""
    response = []
    column = int(column)
    row = int(row)
    f = b[column][row]
    if white(column, row):
        plus = 0
    else:
        plus = 10

    if f == 6: # White's pawn
        if row < 7 and empty(column, row + 1):
            response.append([column,row+1])
        if row == 1 and empty(column, row + 1) and empty(column, row + 2):
            response.append([column,row+2])
        # capture to the right:
        if row < 7 and column < 7 and opposite(column+1,row+1,plus):
            response.append([column+1,row+1])
        # capture to the left:
        if row < 7 and column > 0 and opposite(column-1,row+1,plus):
            response.append([column-1,row+1])
    if f == 16: # Black's pawn
        if row > 0 and empty(column, row - 1):
            response.append([column,row-1])
        if row == 6 and empty(column, row - 1) and empty(column, row - 2):
            response.append([column,row-2])
        # capture to the right:
        if row > 0 and column < 7 and opposite(column+1,row-1,plus):
            response.append([column+1,row-1])
        # capture to the left:
        if row > 0 and column > 0 and opposite(column-1,row-1,plus):
            response.append([column-1,row-1])
    if f == 2 + plus or f == 3 + plus: # queen or rook
        # how long is it possible to move towards right:
        herex = column
        herey = row
        while herex < 7 and empty(herex+1, herey):
            response.append([herex+1,herey])
            herex += 1
        if herex < 7 and opposite(herex+1, herey,plus):
            response.append([herex+1,herey])
        # how long is it possible to move towards left:
        herex = column
        herey = row
        while herex > 0 and empty(herex-1, herey):
            response.append([herex-1,herey])
            herex -= 1
        if herex > 0 and opposite(herex-1, herey,plus):
            response.append([herex-1,herey])
        # how long is it possible to move downwards:
        herex = column
        herey = row
        while herey > 0 and empty(herex, herey-1):
            response.append([herex,herey-1])
            herey -= 1
        if herey > 0 and opposite(herex, herey-1,plus):
            response.append([herex,herey-1])
        # how long is it possible to move upwards:
        herex = column
        herey = row
        while herey < 7 and empty(herex, herey+1):
            response.append([herex,herey+1])
            herey += 1
        if herey < 7 and opposite(herex, herey+1,plus):
            response.append([herex,herey+1])
    if f == 2 + plus or f == 4 + plus: # queen or bishop
        # how long is it possible to move right-upwards:
        herex = column
        herey = row
        while herex < 7 and herey < 7 and empty(herex+1, herey+1):
            response.append([herex+1,herey+1])
            herex += 1
            herey += 1
        if herex < 7 and herey < 7 and opposite(herex+1, herey+1,plus):
            response.append([herex+1,herey+1])
        # how long is it possible to move left-upwards:
        herex = column
        herey = row
        while herex > 0 and herey < 7 and empty(herex-1, herey+1):
            response.append([herex-1,herey+1])
            herex -= 1
            herey += 1
        if herex > 0 and herey < 7 and opposite(herex-1, herey+1,plus):
            response.append([herex-1,herey+1])
        # how long is it possible to move left-downwards:
        herex = column
        herey = row
        while herex > 0 and herey > 0 and empty(herex-1, herey-1):
            response.append([herex-1,herey-1])
            herex -= 1
            herey -= 1
        if herex > 0 and herey > 0 and opposite(herex-1, herey-1,plus):
            response.append([herex-1,herey-1])
        # how long is it possible to move right-downwards:
        herex = column
        herey = row
        while herey > 0 and herex < 7 and empty(herex+1, herey-1):
            response.append([herex+1,herey-1])
            herex += 1
            herey -= 1
        if herey > 0 and herex < 7 and opposite(herex+1, herey-1,plus):
            response.append([herex+1,herey-1])
    if f == 5 + plus: # knight
        if row < 7 and column < 6 and not same(column + 2, row + 1,plus):
            response.append([column+2,row+1])
        if row > 0 and column < 6 and not same(column + 2, row - 1,plus):
            response.append([column+2,row-1])
        if row < 6 and column < 7 and not same(column + 1, row + 2,plus):
            response.append([column+1,row+2])
        if row > 1 and column < 7 and not same(column + 1, row - 2,plus):
            response.append([column+1,row-2])
        if row < 7 and column > 1 and not same(column - 2, row + 1,plus):
            response.append([column-2,row+1])
        if row > 0 and column > 1 and not same(column - 2, row - 1,plus):
            response.append([column-2,row-1])
        if row < 6 and column > 0 and not same(column - 1, row + 2,plus):
            response.append([column-1,row+2])
        if row > 1 and column > 0 and not same(column - 1, row - 2,plus):
            response.append([column-1,row-2])
    if f == 1 + plus: # king
        if row < 7 and column < 7 and not same(column + 1, row + 1,plus):
            response.append([column+1,row+1])
        if row > 0 and column < 7 and not same(column + 1, row - 1,plus):
            response.append([column+1,row-1])
        if row < 7 and column > 0 and not same(column - 1, row + 1,plus):
            response.append([column-1,row+1])
        if row > 0 and column > 0 and not same(column - 1, row - 1,plus):
            response.append([column-1,row-1])
        if column < 7 and not same(column + 1, row,plus):
            response.append([column+1,row])
        if row < 7 and not same(column, row + 1,plus):
            response.append([column,row+1])
        if column > 0 and not same(column - 1, row,plus):
            response.append([column-1,row])
        if row > 0 and not same(column, row - 1,plus):
            response.append([column,row-1])
    return response

def figure_name(f):
    names = {
        1: "K",
        2: "Q",
        3: "R",
        4: "B",
        5: "N",
        6: str("")
        }
    if f > 6:
        f -= 10
    return names.get(f,"?")

def moveinfo(x1,y1,x2,y2):
    f = figure_name(b[int(x1)][int(y1)])
    x = str("")
    if b[int(x2)][int(y2)] > 0:
        x = "x"
        if f == "": # for pawns we store the from column
            f = str(chr(x1+ord('a')))
    return f + x + str(chr(x2+ord('a'))) + str(y2+1)

def to_move_but_not_in_check(column,row):
    global board_value;
    """Compute the list of possible moves for a given player. Moving in check is disallowed."""
    f = b[int(column)][int(row)]
    if white(column, row):
        plus = 0
    else:
        plus = 10

    response = to_move_possible(column,row)
    # We verify if there is a move among the possibe moves that would be in check.
    to_remove = []
    for move in response:
        info = moveinfo(column,row,move[0],move[1])
        # print ("Does the move",info,"imply a check?")
        undoinfo = perform_move(column,row,move[0],move[1]) # let's try what happens if we perform this move
        # Let's check what moves the opponent can have in this case
        for c in range(8):
            for r in range(8):
                if opposite(c,r,plus):
                    for opponent_move in to_move_possible(c,r):
                        info = moveinfo(c,r,opponent_move[0],opponent_move[1])
                        undoinfo2 = perform_move(c,r,opponent_move[0],opponent_move[1])
                        if board_value < -500 or board_value > 500: # the king of one of the players is lost
                            # print("Yes, because opponent's move",info,"implies board value",board_value)
                            if not (move in to_remove):
                                to_remove.append(move) # this move is incorrect, let's remove it
                        undo(undoinfo2) # the opponent's move will be undone
        undo(undoinfo) # our own move will be undone
    for move in to_remove:
        response.remove(move)
    return response

def wins(player):
    pygame.mixer.music.fadeout(0)
    pygame.mixer.music.load(player + "_wins.wav")
    pygame.mixer.music.play(0)
    time.sleep(8)
    pygame.quit()
    sys.exit()

def perform_move(fromx, fromy, tox, toy):
    """Perform a move. Return a list of undo-information, and appends the current board value to the list."""
    global board_value
    board_value_old = board_value
    fromx = int(fromx)
    fromy = int(fromy)

    tox = int(tox)
    toy = int(toy)
    v = []

    values = {
        1: -1000,
        2: -9,
        3: -5,
        4: -3,
        5: -2,
        6: -1,
        11: 1000,
        12: 9,
        13: 5,
        14: 3,
        15: 2,
        16: 1
        }

    target_figure = b[tox][toy]
    # This will be captured:
    board_value -= values.get(target_figure, 0)

    v.append([tox,toy,target_figure]) # store the target figure in the list
    b[tox][toy] = b[fromx][fromy]
    v.append([fromx,fromy,b[fromx][fromy]]) # store the source figure in the list
    b[fromx][fromy] = 0
    # handle promotion of White's pawn (it will be a queen)
    if b[tox][toy] == 6 and toy == 7:
        b[tox][toy] = 2
        board_value -= 8
    # handle promotion of Black's pawn (it will be a queen)
    if b[tox][toy] == 16 and toy == 0:
        b[tox][toy] = 12
        board_value += 8
    v.append([board_value_old])
    return v

def undo(undoinfo):
    """Undo a move and restore the board value."""
    global board_value
    board_value_old = board_value
    for i in undoinfo:
        if len(i) == 3:
            b[i[0]][i[1]] = i[2]
        else:
            board_value = i[0]

def computers_move(from_possible, to_possible):
    global board_value;
    number = len(to_possible)
    best_board_value = -2000 # initial value, we expect a better board value (maximinimax)
    best_move = 0 # if there is no other possibility, use first possible move
    for move in range(number):
        attempt_from = from_possible[move]
        attempt_to = to_possible[move]
        undoinfo = perform_move(attempt_from[0], attempt_from[1], attempt_to[0], attempt_to[1]) # Black's planned move
        # Check White's possible answers...
        white_best_answer = 2000 # initial value, we expect a worse board value (minimax)
        for i in range(8):
            for j in range(8):
                if white(i,j):
                    to_possible2 = to_move_but_not_in_check(i,j)
                    for move2 in to_possible2:
                        undoinfo2 = perform_move(i,j,move2[0],move2[1])
                        # Check Black's possible answers...
                        black_best_response = -2000 # initial value, we expect a better board value (max)
                        for i2 in range(8):
                            for j2 in range(8):
                                if black(i2,j2):
                                    to_possible3 = to_move_but_not_in_check(i2,j2)
                                    for move3 in to_possible3:
                                        undoinfo3 = perform_move(i2,j2,move3[0],move3[1])
                                        if board_value > black_best_response:
                                            black_best_response = board_value
                                        undo(undoinfo3)
                        if black_best_response < white_best_answer:
                            white_best_answer = black_best_response
                        undo(undoinfo2)
        if white_best_answer > best_board_value:
            best_board_value = white_best_answer
            best_move = move
        if white_best_answer == best_board_value and random.randint(1,6) <= 1: # some randomization
            best_move = move
        undo(undoinfo)
    return best_move


selected = False
move_done = False
step = 1
game = ""

opening = { # https://www.shredderchess.com/online/opening-database.html
 "1. e4": [2, 6, 2, 4], # c5
 "1. d4": [6, 7, 5, 5], # Nf6
 "1. Nf3": [6, 7, 5, 5], # Nf6
 "1. c4": [6, 7, 5, 5], # Nf6
 "1. g3": [3, 6, 3, 4], # d5
 "1. b3": [4, 6, 4, 4], # e5
 "1. f4": [3, 6, 3, 4], # d5
 "1. Nc3": [2, 6, 2, 4], # c5
 "1. e4 c5 2. Nf3": [3, 6, 3, 5], # d6
 "1. e4 c5 2. c3": [6, 7, 5, 5], # Nf6
 "1. e4 c5 2. Nc3": [1, 7, 2, 5], # Nc6
 "1. e4 c5 2. Bc4": [4, 6, 4, 5], # e6
 "1. d4 Nf6 2. c4": [4, 6, 4, 5], # e6
 "1. d4 Nf6 2. Nf3": [6, 6, 6, 5], # g6
 "1. d4 Nf6 2. Bg5": [5, 5, 4, 3] # Ne4
 }

while running:

    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            mousebuttons = pygame.mouse.get_pressed()
            if mousebuttons[0]:
                mouse_where = pygame.mouse.get_pos()
                mousex = int((mouse_where[0] - xplus) / square)
                mousey = 7 - int(((mouse_where[1] - yplus) / square))
                if (mousex >= 0) and (mousex <= 7) and (mousey >=0) and (mousey <= 7):
                    if selected:
                        for move in moves:
                            tox = move[0]
                            toy = move[1]
                            if (mousex == tox) and (mousey == toy):
                                # White's move:
                                info = moveinfo(fromx,fromy,mousex,mousey)
                                game += str(step) + ". " + info + " "
                                print("Game:", game)
                                perform_move(fromx,fromy,mousex,mousey)
                                selected = False
                                move_done = True
                                draw_board()
                    if not move_done:
                        figure = b[mousex][mousey]
                        if (figure >= 1) and (figure <= 6):
                            draw_board()
                            draw_figure(mousex, mousey, 20)
                            moves = to_move_but_not_in_check(mousex, mousey)
                            for move in moves:
                                tox = move[0]
                                toy = move[1]
                                draw_figure(tox, toy, 21)
                                selected = True
                            fromx = mousex
                            fromy = mousey

    pygame.display.flip()

    if move_done: # Computer is about to move:
        to_possible = []
        from_possible = []
        for i in range(8):
            for j in range(8):
                if black(i,j):
                    to_possible_verified = to_move_but_not_in_check(i,j)
                    for move in to_possible_verified:
                        to_possible.append(move)
                        from_possible.append([i,j])

        number = len(to_possible)
        print("Black's possible moves:", number, "cases")
        if number == 0:
            wins("white")

        beginning = datetime.datetime.now()
        move = 0
        if step <= 2: # use the opening database at start
            move = opening.get(game.rstrip(), 0)
        if move == 0:
            move_chosen = computers_move(from_possible, to_possible)
            computer_to = to_possible[move_chosen]
            computer_from = from_possible[move_chosen]
        else:
            computer_from = move[0:2]
            computer_to = move[2:4]
        ending = datetime.datetime.now()
        print ("Computation time for the Black's move:", (ending-beginning))

        # Computer performs its move:
        fromx = computer_from[0]
        fromy = computer_from[1]
        draw_figure(fromx,fromy,20)
        pygame.display.flip()
        time.sleep(0.5)
        mousex = computer_to[0]
        mousey = computer_to[1]
        draw_figure(mousex,mousey,21)
        pygame.display.flip()
        time.sleep(0.5)
        info = moveinfo(fromx,fromy,mousex,mousey)
        game += info + " "
        print ("Game:", game)
        perform_move(fromx,fromy,mousex,mousey)
        draw_board()

        pygame.display.flip()

        # Is White checkmated?
        checkmate = True
        for i in range(8):
            for j in range(8):
                if white(i,j):
                    if to_move_but_not_in_check(i,j) != []:
                        checkmate = False
        if checkmate:
            wins("black")

        step += 1

        print ("Board value:", board_value)

    move_done = False

    clock.tick(30)
