from const import *
from square import Square
from piece import *
from move import *
import copy
import os

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLUMNS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        # Extract initial and final positions from the move
        initial = move.initial
        final = move.final

        en_pessant_empty = self.squares[final.row][final.col].is_empty()

        # Update the move on the board
        # Remove the piece from the initial square
        self.squares[initial.row][initial.col].piece = None
        # Place the piece in the final square
        self.squares[final.row][final.col].piece = piece


        if isinstance(piece, Pawn):
            # en pessant capture
            diff = final.col - initial.col 
            # moving diagonally 
            if diff != 0 and en_pessant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece

            else:
                # pawn promotion
                self.check_promotion(piece, final)


        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # Update the piece's moved status to True
        piece.moved = True

        # Clear the piece's previous moves as they are no longer valid
        piece.clear_moves()

        # Store the last move for reference or rendering purposes
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        # if the pwn got to the end row 
        if final.row == 0 or final.row == 7:
            # if it gets there just make it a queen of the color of the pawn
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        # if the king moved by two squares we are castling 
        return abs(initial.col - final.col) == 2
    
    def set_true_en_pessant(self, piece):

        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLUMNS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_pessant = False

        piece.en_pessant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        # move the piece to check if after movement there's a check 
        temp_board.move(temp_piece, move)

        # go thorugh the whole board 
        for row in range(ROWS):
            for col in range(COLUMNS):
                # check if there's an enemy piece
                if temp_board.squares[row][col].has_rivalp(piece.color):
                    p = temp_board.squares[row][col].piece
                    # if there is then calculate moves of this piece; we have false bc we dont wanna move the piece just cal its moves
                    temp_board.calc_moves(p, row, col, bool=False)
                    # loop those moves
                    for m in p.moves:
                        # if it ends with then king then its a check 
                        if isinstance(m.final.piece, King):
                            return True
        # no check
        return False

    # get the valid moves of a psecific piece in a specific loc
    # we addes the bool to avoid infinite loop w in check
    def calc_moves(self, piece, row, col, bool=True):

        def pawn_moves():
            # check if a pawn has actually been moved
            if piece.moved:
                # they cant move two anymore
                steps = 1
            else:
                steps = 2

            # vertical moves 
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            # exclusive 
            for possmove_row in range(start, end, piece.dir):
                if Square.in_range(possmove_row):
                    if self.squares[possmove_row][col].is_empty():
                        # create initial square 
                        initial = Square(row, col)
                        # emnding square 
                        final = Square(possmove_row, col)
                        move = Move(initial, final)

                        # we are calling calc_moves from main class
                        if bool:
                            # check for checks
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                    # if not empty cant eat bc its vertical
                    else:
                        break
                # not in range 
                else:
                    break
            
            # diagonal
            possmove_row = row + piece.dir
            possmove_cols = [col - 1, col + 1]
            for possmove_col in possmove_cols:
                # if it's not out of bounds
                if Square.in_range(possmove_row, possmove_col):
                    # if they have an enemy piece you can eat it diagonally.
                    if self.squares[possmove_row][possmove_col].has_rivalp(piece.color):
                        # c reate intial & target squares
                        initial = Square(row, col)
                        final_piece = self.squares[possmove_row][possmove_col].piece
                        final = Square(possmove_row, possmove_col, final_piece)
                        # make the object of the move
                        move = Move(initial, final)

                        # we are calling calc_moves from main class
                        if bool:
                            # check for checks
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # en pessant
            if piece.color == 'white':
                r = 3
                fr = 2
            else:
                r = 4
                fr = 5
            

            # left en pessant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_rivalp(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_pessant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            # make the object of the move
                            move = Move(initial, final)

                            # we are calling calc_moves from main class
                            if bool:
                                # check for checks
                                if not self.in_check(piece, move):
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)
            
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_rivalp(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_pessant:
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            # make the object of the move
                            move = Move(initial, final)

                            # we are calling calc_moves from main class
                            if bool:
                                # check for checks
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

        def knight_moves():
            # if there's nothing then 8 moves
            possible_moves = [
                (row + 2, col - 1), 
                (row - 2, col - 1),
                (row + 2, col + 1), 
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row - 1, col - 2),
                (row + 1, col - 2),
            ]

            for pmove in possible_moves:
                pmove_row, pmove_col = pmove

                if Square.in_range(pmove_row, pmove_col):
                    # if the piece we reicve is empty or hs a rival (valid moves)
                    if self.squares[pmove_row][pmove_col].isempty_or_rival(piece.color):
                        # method 
                        initial = Square(row, col)
                        final_piece = self.squares[pmove_row][pmove_col].piece
                        final = Square(pmove_row, pmove_col, final_piece)
                        # create the new move 
                        move = Move(initial, final)

                        # we are calling calc_moves from main class
                        if bool:
                            # check for checks
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def straightline_moves(increments):
            for inc in increments:
                row_inc, col_inc = inc
                possmove_row = row + row_inc
                possmove_col = col + col_inc

                while True:
                    if Square.in_range(possmove_row, possmove_col):
                        # create squares of poss new move
                        initial = Square(row, col)
                        final_piece = self.squares[possmove_row][possmove_col].piece
                        final = Square(possmove_row, possmove_col, final_piece)
                        move = Move(initial, final)

                        # if its empty, we do them different bc we can keep checking increments
                        if self.squares[possmove_row][possmove_col].is_empty():
                            # we are calling calc_moves from main class
                            if bool:
                                # check for checks
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                                else:
                                    break
                            else:
                                piece.add_move(move)
                            # continue looping 
                    
                        # if it has enemy piece, we cut to see if we wanna eat it 
                        elif self.squares[possmove_row][possmove_col].has_rivalp(piece.color):
                            if bool:
                                # check for checks
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            # break it 
                            break 

                        # has team piece 
                        elif self.squares[possmove_row][possmove_col].has_teamp(piece.color):
                            # dont use it as a move just break 
                            break
                    else:
                        break 
                        
                    # increment the increments 
                    possmove_row = possmove_row + row_inc
                    possmove_col = possmove_col + col_inc

        def king_moves():
            adj_moves = [
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1),
                (row + 1, col + 0), 
                (row - 1, col + 0), 
                (row + 1, col + 1), 
                (row + 0, col + 1), 
                (row - 1, col + 1)
            ]

            for adj in adj_moves:
                # separate the touple
                adj_row, adj_col = adj
                if Square.in_range(adj_row, adj_col):
                    # if its empty or it allws for a move 
                    if self.squares[adj_row][adj_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(adj_row, adj_col)
                        # create a move with that 
                        move = Move(initial, final)

                        # we are calling calc_moves from main class
                        if bool:
                            # check for checks
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
            
            # castling moves allow it
            # if kiinng hasnt moved
            if not piece.moved: 
                # queen castling
                # we assume rook hasnt moved
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    # if it hasnt moved
                    if not left_rook.moved:
                        # kmake a loop to see if there spots between are empty
                        for c in range (1, 4):
                            if self.squares[row][c].has_piece():
                                # not valid
                                break
                            
                            if c == 3:
                                # addsa left rook to king
                                piece.left_rook = left_rook
                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                if bool:
                                # check for checks
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
                
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    # if it hasnt moved
                    if not right_rook.moved:
                        # kmake a loop to see if there spots between are empty
                        for c in range (5, 7):
                            if self.squares[row][c].has_piece():
                                # not valid
                                break
                            
                            if c == 6:
                                # addsa left rook to king
                                piece.right_rook = right_rook
                                #rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                if bool:
                                # check for checks
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)

        # the same as if piece.pawn, so if it exists
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), # upper right
                (-1, -1), # upper left
                (1, 1), # down right
                (1, -1) # down left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), # up
                (1, 0), # down
                (0, -1), # left
                (0, 1) # right
            ])

        elif isinstance(piece, King):
            king_moves()

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 0), # up
                (1, 0), # down
                (0, -1), # left
                (0, 1), # right
                (-1, 1), # upper right
                (-1, -1), # upper left
                (1, 1), # down right
                (1, -1) # down left
            ])

    def _create(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLUMNS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))