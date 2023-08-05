"""
Date: 13 May 2022
Author: Akshay Ranade

The graphics related code was getting very complicated to address stuff like
window resizing, text boxes, timer etc. So, it was decided to create a class
for doing this.
"""

import pygame as p
import pygame_textinput as pt


min_width = 640
min_height = 480
dimension = 8
min_sq_size = (min_height // 12)

class graphics:
    """
    Class to handle all complex graphics related functionalities.
    """

    def __init__(self, gs):
        self.gs = gs
        p.init()
        self.initial_parameters()
        self.running = True
        self.run()

    def __init__(self, gs, rating, timer):
        self.gs = gs
        p.init()
        self.initial_parameters(rating, timer)
        self.running = True
        self.run()

    def run(self):
        while self.running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.running = False
                if e.type == p.VIDEORESIZE:
                    width, height = self.screen.get_size()
                    self.width = max(width, min_width)
                    self.height = max(height, min_height)
                    self.sq_size = self.height // 12
                    self.screen = p.display.set_mode((self.width, self.height), self.flags)
                    self.screen.fill(p.Color("brown"))
                if e.type == p.MOUSEBUTTONDOWN:
                    click_x, click_y = p.mouse.get_pos()
                    # next button
                    self.next_button_clicked = self.next_button_rect.collidepoint(click_x, click_y)
                    # rating text input
                    if self.rating_rect.collidepoint(click_x, click_y):
                        self.rating_textbox_selected = True
                        print("here")
                    else:
                        self.rating_textbox_selected = False
                    # timer text input
                    if self.timer_rect.collidepoint(click_x, click_y):
                        self.timer_textbox_selected = True
                    else:
                        self.timer_textbox_selected = False
                if self.rating_textbox_selected:
                    if e.type == p.KEYDOWN:
                        print(e.unicode)
                        if e.key == p.K_BACKSPACE:
                            self.rating_str = self.rating_str[:-1]
                        elif e.unicode.isdigit():
                            self.rating_str += e.unicode
                            self.rating_str = str(min(3000, int(self.rating_str)))
                        print(self.rating_str)
                if self.timer_textbox_selected:
                    if e.type == p.KEYDOWN:
                        if e.key == p.K_BACKSPACE:
                            self.timer_str = self.timer_str[:-1]
                        elif e.unicode.isdigit():
                            self.timer_str += e.unicode
                            self.timer_str = str(min(60, int(self.timer_str)))
                if e.type == p.MOUSEBUTTONUP:
                    self.next_button_clicked = False
                if e.type == p.USEREVENT:
                    time_remaining = int(self.countdown_str) - 1
                    time_remaining = max(0, time_remaining)
                    self.countdown_str = str(time_remaining)
                if self.next_button_clicked:
                    self.running = False

            self.draw_board()
            self.draw_pieces()
            self.draw_side_panel()
            self.clock.tick(self.max_fps)
            p.display.flip()


    def initial_parameters(self, rating='1500', timer='10'):
        # size parameters
        self.width = min_width
        self.height = min_height
        self.sq_size = self.height // 12

        # drawing the initial window
        self.flags = p.RESIZABLE
        self.screen = p.display.set_mode((self.width, self.height), self.flags)
        p.display.set_caption('Chess Occlusion Training')
        self.screen.fill(p.Color("brown"))
        self.clock = p.time.Clock()
        self.max_fps = 15

        # load chess set and save in memory
        self.load_chessmen()

        # control flags
        self.next_button_clicked = False
        self.rating_textbox_selected = False
        self.timer_textbox_selected = False

        # variables and default values for text inputs
        self.rating_str = rating
        self.timer_str = timer

        # event required for the actual countdown timer
        p.time.set_timer(p.USEREVENT, 1000)
        self.countdown_str = self.timer_str
        self.timer_duration = int(self.timer_str)
    def load_chessmen(self):
        """
        Loads images of all pieces for both colours from disk. Called from the main function.
        For now we have just one set of pieces, but we can add others in the future. Choice of pieces
        can be offered to the user in main and then this function will take that choice as input.
        """
        self.chessmen = {}
        colours = ['b', 'w']
        piece_types = ['R', 'N', 'B', 'Q', 'K', 'P']
        pieces = [col + piece_type for col in colours for piece_type in piece_types]
        for piece in pieces:
            self.chessmen[piece] = p.image.load("../data/images/" + piece + ".svg")

    def draw_board(self):
        """
        Helper function to draw the background.
        """

        # trying to get the board "centred"...need to play around with the offset_factor
        # basically, the idea is for the graphics to look "nice" when window is resized
        offset_factor = 10
        self.left_offset = self.width // offset_factor
        self.top_offset = self.height // offset_factor
        sq_size = self.sq_size
        colors = [p.Color("white"), p.Color("gray")]

        if self.timer_duration == '0':
            p.draw.rect(self.screen, p.Color(0,0,0),
                        p.Rect(self.left_offset, self.top_offset, 8*sq_size, 8*sq_size))
        else:
            for row in range(dimension):
                for col in range(dimension):
                    # draw the board and background
                    color = colors[(row + col) % 2]
                    left = self.left_offset + col * sq_size
                    top = self.top_offset + row * sq_size
                    p.draw.rect(self.screen, color, p.Rect(left, top, sq_size, sq_size))




    def draw_pieces(self):
        """
        Helper function to draw the pieces from a given game state.
        """
        if self.timer_duration != '0':
            sq_size = self.sq_size
            for row in range(dimension):
                for col in range(dimension):
                    piece = self.gs.board[row][col]
                    if not piece == "--":
                        image = p.transform.scale(self.chessmen[piece], (0.8*sq_size, 0.8*sq_size))
                        left = self.left_offset + col * sq_size
                        top = self.top_offset + row * sq_size
                        piece_offset = sq_size/10
                        self.screen.blit(image, p.Rect(left+piece_offset, top+piece_offset, sq_size, sq_size))

    def draw_side_panel(self):
        """
        Helper function to draw the panel beside the chess board.
        """
        # sq_size depends on the window size
        sq_size = self.sq_size
        # make sure that font_size is flexibly defined so that text is also scaled on window resize
        base_font_size = 20
        font_size = base_font_size * self.sq_size // min_sq_size
        # get the coordinates of the top right square of the board
        board_top_right_x = self.left_offset + 8 * sq_size
        board_top_right_y = self.top_offset

        # draw the panel background
        p.draw.rect(self.screen, p.Color("black"),
                    p.Rect(board_top_right_x, board_top_right_y, sq_size // 16, 8 * sq_size ))
        p.draw.rect(self.screen, p.Color("white"),
                    p.Rect(self.left_offset + (8+1/16) * sq_size, self.top_offset, 4 * sq_size, 8 * sq_size))


        # Write Caissa at the top of the side panel
        font = p.font.SysFont(None, font_size)
        text = font.render("Caissa",True, p.Color("blue"))
        self.screen.blit(text, (board_top_right_x + sq_size, board_top_right_y + sq_size//10))

        # Write which side is to move
        font_small = p.font.SysFont(None, 3 * (font_size//5))
        if self.gs.side_to_move == 'w':
            text = font_small.render("White to move", True, p.Color("black"))
        else:
            text = font_small.render("Black to move", True, p.Color("black"))
        self.screen.blit(text, (board_top_right_x + 3*sq_size//4, board_top_right_y + sq_size//2) )
        text = font_small.render("Board is from White's perspective!", True, p.Color("black"))
        self.screen.blit(text, (board_top_right_x + sq_size // 10, board_top_right_y + 3 * sq_size // 4))

        # create input box prompts
        ## rating begin
        left = board_top_right_x + (1/2 + 1/16) * sq_size
        top = board_top_right_y + 2 * sq_size
        text_rating = font.render("Rating", True, p.Color((40, 20, 20)))
        self.screen.blit(text_rating, (left,top))
        self.rating_rect = p.Rect(left + 1.1 * text_rating.get_width(), top, sq_size, sq_size / 2)
        if self.rating_textbox_selected:
            p.draw.rect(self.screen, p.Color('aquamarine4'),
                    self.rating_rect)
        else:
            p.draw.rect(self.screen, p.Color('aquamarine3'),
                        self.rating_rect)
        # show the inputted rating on the screen
        rating_text = font.render(self.rating_str, True, p.Color((20,20,20)))
        self.screen.blit(rating_text,(self.rating_rect.x + sq_size/10, self.rating_rect.y + sq_size/20))
        ## rating end
        #
        ## timer begin
        top = board_top_right_y + 3 * sq_size
        text_timer = font.render("Timer", True, p.Color((40, 20, 20)))
        self.screen.blit(text_timer, (left, top))
        self.timer_rect = p.Rect(left + 1.1 * text_timer.get_width(), top, sq_size / 2, sq_size / 2)
        if self.timer_textbox_selected:
            p.draw.rect(self.screen, p.Color('aquamarine4'),
                    self.timer_rect)
        else:
            p.draw.rect(self.screen, p.Color('aquamarine3'),
                        self.timer_rect)
        # show the inputted rating on the screen
        timer_text = font.render(self.timer_str, True, p.Color((20, 20, 20)))
        self.screen.blit(timer_text, (self.timer_rect.x + sq_size / 15, self.timer_rect.y + sq_size / 20))
        ## timer end

        # Create button for next puzzle
        left = board_top_right_x + (1/2 + 1/16) * sq_size
        top = board_top_right_y + 4 * sq_size
        width = 1 * sq_size
        height = sq_size / 1.75
        # we save therectangle to check for mouse button events
        self.next_button_rect = p.Rect(left, top, width, height)

        if self.next_button_clicked:
            p.draw.rect(self.screen, p.Color('aquamarine4'),
                        self.next_button_rect)
        else:
            p.draw.rect(self.screen, p.Color('aquamarine3'),
                        self.next_button_rect)
        text = font.render("Next", True, p.Color((40, 20, 20)))
        self.screen.blit(text, (left+width/10, top + height/10))



        # countdown
        self.timer_duration =  (self.countdown_str)    # None if self.countdown_str == ''  else
        left = self.timer_rect.left + self.sq_size / 2
        top = self.timer_rect.top
        p.draw.rect(self.screen, p.Color('blue'), p.Rect(left, top, self.sq_size / 2, self.sq_size / 2))
        text_countdown = font.render(self.countdown_str, True, p.Color(230, 230, 230))
        self.screen.blit(text_countdown, (left+width/10, top+height/10))

        
