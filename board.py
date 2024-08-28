import pygame

class Square:
    def __init__(self, row, col, color, size):
        self.row = row
        self.col = col
        self.color = color
        self.piece = None
        self.x = col * size
        self.y = row * size

    def draw(self, screen, size):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, size, size))
        if self.piece:
            self.piece.draw(screen, self.x, self.y)


class Board:
    def __init__(self, size):
        self.size = size
        self.squares = self.create_board()
        
    def create_board(self):
        LIGHT_BROWN = (240, 217, 181)
        DARK_BROWN = (181, 136, 99)

        colors = [LIGHT_BROWN, DARK_BROWN]
        board = []
        for row in range(8):
            board_row = []
            for col in range(8):
                color = colors[(row + col) % 2]
                board_row.append(Square(row, col, color, self.size))
            board.append(board_row)
        return board
    
    def get_king_position(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.name == 'king' and piece.color == color:
                    return row, col
        return None
    
    def initialize_pieces(self):
        from pieces import King, Queen, Rook, Bishop, Knight, Pawn
        pieces = [
            Rook('white', (7, 0)), Knight('white', (7, 1)), Bishop('white', (7, 2)), Queen('white', (7, 3)), King('white', (7, 4)), Bishop('white', (7, 5)), Knight('white', (7, 6)), Rook('white', (7, 7)),
            *[Pawn('white', (6, col)) for col in range(8)],
            Rook('black', (0, 0)), Knight('black', (0, 1)), Bishop('black', (0, 2)), Queen('black', (0, 3)), King('black', (0, 4)), Bishop('black', (0, 5)), Knight('black', (0, 6)), Rook('black', (0, 7)),
            *[Pawn('black', (1, col)) for col in range(8)],
        ]

        for piece in pieces:
            row, col = piece.position
            self.squares[row][col].piece = piece
    
    def get_piece(self, row, col):
        return self.squares[row][col].piece

    def draw(self, screen):
        for row in self.squares:
            for square in row:
                square.draw(screen, self.size)
    
    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.get_piece(start_row, start_col)
        if piece:
            self.squares[end_row][end_col].piece = piece 
            self.squares[start_row][start_col].piece = None
        else:
            print("No piece at the starting position")

    def highlight_moves(self, screen, moves):
        GREEN = (0, 255, 0)
        for move in moves:
            row, col = move
            square = self.squares[row][col]
            center_x = square.x + self.size // 2
            center_y = square.y + self.size // 2
            radius = self.size // 4
            pygame.draw.circle(screen, GREEN, (center_x, center_y), radius)
