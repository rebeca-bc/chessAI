import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        # initialize pygame model
        pygame.init()
        # create a pygame screen w consts
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainLoop(self):

        # simplify calls
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_bg(screen)      
            game.show_last_move(screen)      
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            # loop through all events to see if user is quitting
            for event in pygame.event.get():
                
                # click on piece
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # send the position where we are clicking
                    dragger.update_mouse(event.pos)
                    # check if position has a piece
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    # if there something save and continue
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # if it's valid piece color to drag
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            # send the piece to start dragging
                            dragger.drag_piece(piece)
                            # show methods & carfeul w order
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)


                # moving mouse to drag
                elif event.type == pygame.MOUSEMOTION:
                    # check if there's actually somthing being dragged
                    if dragger.dragging:
                        # update mouse
                        dragger.update_mouse(event.pos)
                        # show bg and other while moving
                        game.show_bg(screen)
                        # show the possible moves
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        # update the bit bc it depends on mouse
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:  # Check if there's a piece being dragged
                        # Update the mouse position
                        dragger.update_mouse(event.pos)
                        
                        # Calculate the row and column where the mouse was released
                        release_row = dragger.mouseY // SQSIZE
                        release_col = dragger.mouseX // SQSIZE

                        # Create a possible move based on the initial and final positions
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(release_row, release_col)
                        move = Move(initial, final)

                        # Check if the move is valid according to the game rules
                        if board.valid_move(dragger.piece, move):

                            # If the move is valid, execute the move on the board
                            board.move(dragger.piece, move)

                            board.set_true_en_pessant(dragger.piece)

                            # Update the display to show the new board state after the move
                            game.show_bg(screen)
                            # it has to be below the pieces but top of bg
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # next turn 
                            game.next_turn()

                    # End the dragging operation (even if no valid move was made)
                    dragger.undrag_piece()

                # if a key is pressed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        screen = self.screen
                        dragger = self.game.dragger
                        board = self.game.board
                    
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                # if quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

# create an instance
main = Main()
main.mainLoop()
