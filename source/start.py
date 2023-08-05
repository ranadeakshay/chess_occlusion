"""
Date : 06 May 2022
Author : Akshay Ranade

The original plan was to try and use the API to get puzzles one by one.
However, this functionality is not available in the API. Instead, all puzzles
are available in one big database. So, the plan now is to simply use the database
to draw puzzles one at a time filtered by some user inputs. The filters include
puzzle rating, puzzle tags, number of moves in solution etc.

Credits:
1. Eddie Sharick's youtube channel : I learnt some of the pygame stuff from one of his tutorials
"""
import random

import pandas as pd
import pygame as p
from game import game_state
from graphics import graphics
import os

# parameters for pygame
width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}


# load images as a global dictionary.
def load_images():
    """
    Loads images of all pieces for both colours from disk. Called from the main function.
    For now we have just one set of pieces, but we can add others in the future. Choice of pieces
    can be offered to the user in main and then this function will take that choice as input.
    """
    colours = ['b', 'w']
    piece_types = ['R', 'N', 'B', 'Q', 'K', 'P']
    pieces = [col + piece_type for col in colours for piece_type in piece_types]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("../data/images/" + piece + ".asvg"), (sq_size, sq_size))


def draw_board(screen):
    """
    Helper function to draw the background.
    """
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(dimension):
        for col in range(dimension):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * sq_size, row * sq_size, sq_size, sq_size))


def draw_pieces(screen, gs):
    """
    Helper function to draw the pieces from a given game state.
    """
    for row in range(dimension):
        for col in range(dimension):
            piece = gs.board[row][col]
            if not piece == "--":
                screen.blit(images[piece], p.Rect(col * sq_size, row * sq_size, sq_size, sq_size))


def draw_graphics(screen, gs):
    """
    Responsible for all the graphics. Relies on two helper functions to draw the background
    and the pieces. Additional functionality like highlighting squares, showing possible moves
    of pieces can be added as additional helper functions.
    """
    draw_board(screen)
    draw_pieces(screen, gs)


# noinspection PyInterpreter
def main():
    print("boo")
    print(os.getcwd())
    print("hoo")
    # load puzzles from database and allow user to choose
    puzzles = pd.read_csv("../data/lichess_db_puzzle.csv")
    """
    TODO: user prompt and inputs for allowing puzzle selection by rating or themes.
    """

    starting_puzzle = random.choice(range(len(puzzles)))
    fen = puzzles.loc[starting_puzzle, 'FEN']  # for now we take the first puzzle
    print(fen)
    # create game_state object from given fen position
    gs = game_state(fen)
    a = graphics(gs, '1500', '10')
    print("that part is done now!", a.next_button_clicked)
    while a.next_button_clicked:
        rated_puzzles = puzzles[
            (puzzles['Rating'] < int(a.rating_str) + 25) & (puzzles['Rating'] > int(a.rating_str) - 25)]
        selected_puzzle = rated_puzzles.sample()
        fen = (selected_puzzle['FEN'].values)[0]
        game_url = selected_puzzle['GameUrl']
        print(game_url)
        # fen = (rated_puzzles.sample()).iloc[0,1]
        gs = game_state(fen)
        a = graphics(gs, a.rating_str, a.timer_str)


if __name__ == "__main__":
    main()
