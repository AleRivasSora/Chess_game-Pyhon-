import pygame

class Piece:
    def __init__(self,color,position):
        self.color = color
        self.image = self.getImage()
        self.position = position
        self.name = type(self).__name__.lower()
        
    def update_position(self, new_position):
        self.position = new_position
    

    def getImage(self):
        if self.color == 'white':
            if type(self) == King:
                return pygame.image.load('static/img/white_king.png')
            elif type(self) == Queen:
                return pygame.image.load('static/img/white_queen.png')
            elif type(self) == Rook:
                return pygame.image.load('static/img/white_rook.png')
            elif type(self) == Bishop:
                return pygame.image.load('static/img/white_bishop.png')
            elif type(self) == Knight:
                return pygame.image.load('static/img/white_knight.png')
            elif type(self) == Pawn:
                return pygame.image.load('static/img/white_pawn.png')
        elif self.color == 'black':
            if type(self) == King:
                return pygame.image.load('static/img/black_king.png')
            elif type(self) == Queen:
                return pygame.image.load('static/img/black_queen.png')
            elif type(self) == Rook:
                return pygame.image.load('static/img/black_rook.png')
            elif type(self) == Bishop:
                return pygame.image.load('static/img/black_bishop.png')
            elif type(self) == Knight:
                return pygame.image.load('static/img/black_knight.png')
            elif type(self) == Pawn:
                return pygame.image.load('static/img/black_pawn.png')

    def legal_moves(self,position,board,game=None):
        pass
    
    def draw(self, screen, x, y):
        offset_x = 7  
        offset_y = 7  
        screen.blit(self.image, (x + offset_x, y + offset_y))

class King(Piece):
    def __init__(self,color, position):
        super().__init__(color, position)

    def legal_moves(self,position,board,game=None):
        row, col = position
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Verificar límites del tablero
                target_square = board[new_row][new_col]
                if target_square.piece is None or target_square.piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class Queen(Piece):
    def __init__(self,color, position):
        super().__init__(color, position)

    def legal_moves(self,position,board,game=None):
        row, col = position
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_square = board[new_row][new_col]
                if target_square.piece is None:
                    moves.append((new_row, new_col))
                elif target_square.piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        
        return moves

class Rook(Piece):
    def __init__(self,color, position):
        super().__init__(color, position )

    def legal_moves(self,position,board,game=None):
        row, col = position
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_square = board[new_row][new_col]
                if target_square.piece is None:
                    moves.append((new_row, new_col))
                elif target_square.piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        
        return moves

class Bishop(Piece):
    def __init__(self,color, position):
        super().__init__(color, position )

    def legal_moves(self,position,board,game=None):
        row, col = position
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Movimientos diagonales

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_square = board[new_row][new_col]
                if target_square.piece is None:
                    moves.append((new_row, new_col))
                elif target_square.piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        
        return moves

class Knight(Piece):
    def __init__(self,color, position):
        super().__init__(color, position )

    def legal_moves(self,position,board,game=None):
        row, col = position
        moves = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_square = board[new_row][new_col]
                if target_square.piece is None or target_square.piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class Pawn(Piece):
    def __init__(self,color, position):
        super().__init__(color, position )

    def legal_moves(self,position,board,game=None):
        row, col = position
        moves = []
        direction = -1 if self.color == 'white' else 1
        

       
        if 0 <= row + direction < 8 and board[row + direction][col].piece is None:
            moves.append((row + direction, col))

         
            if (self.color == 'white' and row == 6) or (self.color == 'black' and row == 1):
                if board[row + 2 * direction][col].piece is None:
                    moves.append((row + 2 * direction, col))

     
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= row + direction < 8 and 0 <= new_col < 8:
                target_square = board[row + direction][new_col]
                if target_square.piece is not None and target_square.piece.color != self.color:
                    moves.append((row + direction, new_col))

        if game is not None and game.last_move:
            if game.last_move:
                last_start, last_end = game.last_move
                last_row, last_col = last_end
                if abs(last_start[0] - last_end[0]) == 2 and board[last_row][last_col].piece.color != self.color:
                    if last_row == row and abs(last_col - col) == 1:
                        moves.append((row + direction, last_col))

        return moves


def load_image(name):
    try:
        image = pygame.image.load(name)
        return image
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        raise SystemExit(e)








