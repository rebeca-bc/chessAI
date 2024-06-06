import pygame

from const import * 
from board import Board
from dragger import Dragger

# class responsible of rendering methods
class Game:
    def __init__(self):
        self.next_player = 'white'
        # create a new board
        self.board = Board()
        self.dragger = Dragger()

    # help draw the board
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if((row+col)%2 == 0):
                    # light blue
                    color = (186,225,255) 
                else:
                    # dark blue
                    color = (18,18,105) 

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                # is there a piece on a specific sq
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    #blit all excpet dragger piece
                    if piece is not self.dragger.piece:
                        # state that if it isnt dragged call of texture to go back to normal
                        piece.set_texture(size=80)
                        # convert tecture into an image
                        img = pygame.image.load(piece.texture)
                        # to make it more centered in the square
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        # show the image into the texture_rect
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        # if we are dragging show moves
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit 
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface): # fix this
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                if((pos.row + pos.col)%2 == 0):
                    # light blue
                    color = (186,225,255) 
                else:
                    # dark blue
                    color = (18,18,105) 

                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        if self.next_player == 'black':
            self.next_player = 'white'
        else:
            self.next_player = 'black'

    def reset(self):
        # create a new game
        self.__init__()
