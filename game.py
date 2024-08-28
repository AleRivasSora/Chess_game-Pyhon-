from board import Board
import pygame
from pieces import King, Pawn
import time

class Game:
    def __init__(self, board_size):
        self.board = Board(board_size)
        self.turn = 'white'
        self.history = []
        self.piece_selected = None
        self.legal_moves = []
        self.white_time = 300  
        self.black_time = 300  
        self.increment = 3  
        self.last_move_time = time.time()
        self.first_move_made = False
        self.last_move = None
        

    def switch_turn(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_move_time
        if self.turn == 'white':
            self.white_time -= elapsed_time
            self.white_time += self.increment
        else:
            self.black_time -= elapsed_time
            self.black_time += self.increment
        self.last_move_time = current_time
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.first_move_made = True

    def record_move(self, move):
        self.history.append(move)

    def draw(self, screen):
        self.board.draw(screen)
        self.is_in_check('white', screen)
        self.is_in_check('black', screen)
        if self.legal_moves:
            for move in self.legal_moves:
                row, col = move
                pygame.draw.circle(screen, (0, 255, 0), (col * self.board.size + self.board.size // 2, row * self.board.size + self.board.size // 2), 15)
        self.draw_clock(screen)

    def get_square_under_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos
        if x < 0 or x >= self.board.size * 8 or y < 0 or y >= self.board.size * 8:
            return None
        row = y // self.board.size
        col = x // self.board.size
        return row, col

    def handle_piece_selection(self, row, col, screen):
        piece = self.board.get_piece(row, col)
        
        if self.piece_selected:
            if self.piece_selected == piece or (piece is None and (row, col) not in self.legal_moves):
                self.piece_selected = None
                self.legal_moves = []
                print("Deseleccionando pieza")
                return
            elif (row, col) in self.legal_moves:
                self.execute_move(self.piece_selected.position[0], self.piece_selected.position[1], row, col)
                return

        if piece and piece.color == self.turn:
            self.piece_selected = piece
            all_legal_moves = piece.legal_moves((row, col), self.board.squares,self)
            self.legal_moves = [move for move in all_legal_moves if not self.move_leaves_king_in_check(piece, move)]
            print(f"Legal moves: {self.legal_moves}")  
        else:
            print("Invalid selection or not your turn")

    def move_leaves_king_in_check(self, piece, move):
        start_row, start_col = piece.position
        end_row, end_col = move


        target_piece = self.board.get_piece(end_row, end_col)
        original_position = piece.position


        self.board.squares[start_row][start_col].piece = None
        self.board.squares[end_row][end_col].piece = piece
        piece.position = (end_row, end_col)

 
        in_check = self.is_in_check(piece.color)


        self.board.squares[start_row][start_col].piece = piece
        self.board.squares[end_row][end_col].piece = target_piece
        piece.position = original_position

        return in_check

    def convert_to_chess_notation(self, row, col):
        columns = 'abcdefgh'
        rows = '87654321'
        return f"{columns[col]}{rows[row]}"

    def convert_from_chess_notation(self, notation):
        columns = 'abcdefgh'
        rows = '87654321'
        col = columns.index(notation[0])
        row = rows.index(notation[1])
        return row, col
    
    def execute_move(self, start_row, start_col, end_row, end_col):
        piece = self.board.get_piece(start_row, start_col)
        
        if piece and (end_row, end_col) in self.legal_moves:
            
            if isinstance(piece, Pawn) and start_col != end_col and self.board.get_piece(end_row, end_col) is None:
                if piece.color == 'white':
                    captured_row = end_row + 1
                else:
                    captured_row = end_row - 1
                self.board.squares[captured_row][end_col].piece = None

            self.board.move_piece(start_row, start_col, end_row, end_col)
            piece.update_position((end_row, end_col))  
            self.record_move(((start_row, start_col), (end_row, end_col)))
            self.last_move = ((start_row, start_col), (end_row, end_col))
            self.switch_turn()
            self.piece_selected = None
            self.legal_moves = []
            print(f"Moved {piece} to {(end_row, end_col)}")
        else:
            print("Invalid move")
    
    def is_in_check(self, color, screen=None):
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:
            return False

        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    if king_position in piece.legal_moves((row, col), self.board.squares):
                        if screen:
                            self.highlight_king_in_check(screen, king_position)
                        return True
        return False
    
    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    legal_moves = piece.legal_moves((row, col), self.board.squares)
                    for move in legal_moves:
                        if not self.move_leaves_king_in_check(piece, move):
                            return False
        return True
    
    def highlight_king_in_check(self, screen, king_position):
        row, col = king_position
        square_size = self.board.size  
        rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)  
        
    def highlight_check(self, screen):
        if self.is_in_check('white'):
            king_position = self.board.get_king_position('white')
            self.highlight_king_in_check(screen, king_position)
        if self.is_in_check('black'):
            king_position = self.board.get_king_position('black')
            self.highlight_king_in_check(screen, king_position)

    def draw_clock(self, screen):
        font = pygame.font.SysFont(None, 36)
        white_minutes = int(self.white_time // 60)
        white_seconds = int(self.white_time % 60)
        black_minutes = int(self.black_time // 60)
        black_seconds = int(self.black_time % 60)
        white_time_text = font.render(f"White: {white_minutes:02}:{white_seconds:02} +3s", True, (255, 255, 255))
        black_time_text = font.render(f"Black: {black_minutes:02}:{black_seconds:02} +3s", True, (255, 255, 255))
        screen.blit(white_time_text, (650, 100))
        screen.blit(black_time_text, (650, 50))
    
