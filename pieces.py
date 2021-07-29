import pygame
from config import *


class Piece(pygame.sprite.Sprite):
    def __init__(self, cell_size, color, field_name, piece_name):
        super().__init__()
        picture = pygame.image.load(SPRITE_PATH + color + piece_name)
        self.image = pygame.transform.scale(picture, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.color = color
        self.field_name = field_name

    def move_to_cell(self, cell):
        self.rect = cell.rect.copy()
        self.field_name = cell.field_name


class King(Piece):
    def __init__(self, cell_size, color, field):
        super().__init__(cell_size, color, field, '_king.png')


class Queen(Piece):
    def __init__(self, cell_size, color, field):
        super().__init__(cell_size, color, field, '_queen.png')


class Rook(Piece):
    def __init__(self, cell_size, color, field):
        super().__init__(cell_size, color, field, '_rook.png')


class Bishop(Piece):
    def __init__(self, cell_size, color, field):
        super().__init__(cell_size, color, field, '_bishop.png')


class Knight(Piece):
    def __init__(self, cell_size, color, field):
        super().__init__(cell_size, color, field, '_knight.png')


class Pawn(Piece):
    def __init__(self, cell_size, color, field):
        super().__init__(cell_size, color, field, '_pawn.png')
