import start_board
from pieces import *

pygame.init()
FONT = pygame.font.Font('C:\Windows\Fonts\ARIALNB.TTF', 18)


class Game_Board:
    def __init__(self, parent_surface: pygame.Surface):
        self.screen = parent_surface
        self.qty_cells = QTY_CELLS
        self.cell_size = CELL_SIZE
        self.start_board = start_board.board
        self.all_cells = pygame.sprite.Group()
        self.all_pieces = pygame.sprite.Group()
        self.all_areas = pygame.sprite.Group()
        self.piece_types = PIECES_TYPE
        self.pressed_cell = None
        self.picked_piece = None
        self.dragged_piece = None
        self.load_background()
        self.draw_board()
        self.setup()
        self.update_all()

    def load_background(self):
        table_img = pygame.image.load('images/table_bg.jpg')
        table_img = pygame.transform.scale(table_img, SIZE)
        self.screen.blit(table_img, (0, 0))

    def draw_board(self):
        board_width = self.qty_cells * self.cell_size
        fields_num = self.create_fields()
        self.all_cells = self.create_cells()
        fields_num_depth = fields_num[0].get_width()
        board_view = pygame.Surface(
            (2 * fields_num_depth + board_width, 2 * fields_num_depth + board_width))
        board_bg = pygame.image.load('images/board_bg.jpg')
        board_bg = pygame.transform.scale(board_bg, (board_view.get_width(), board_view.get_height()))
        board_view.blit(board_bg, board_bg.get_rect())

        board_view.blit(fields_num[0], (0, fields_num_depth))
        board_view.blit(fields_num[0], (fields_num_depth + board_width, fields_num_depth))
        board_view.blit(fields_num[1], (fields_num_depth, 0))
        board_view.blit(fields_num[1], (fields_num_depth, fields_num_depth + board_width))

        board_rect = board_view.get_rect()
        board_rect.x += (self.screen.get_width() - board_rect.width) // 2
        board_rect.y += (self.screen.get_height() - board_rect.height) // 2
        self.screen.blit(board_view, board_rect)
        cells_offset = (board_rect.x + fields_num_depth, board_rect.y + fields_num_depth)
        self.draw_cells_on_board(cells_offset)

    def create_fields(self):
        lines = pygame.Surface((self.qty_cells * self.cell_size, self.cell_size // 2))
        rows = pygame.Surface((self.cell_size // 2, self.cell_size * self.qty_cells))
        for i in range(0, self.qty_cells):
            cell_letter = FONT.render(LETTERS_NAME[i], True, WHITE)
            cell_number = FONT.render(str(QTY_CELLS - i), True, WHITE)
            lines.blit(cell_letter, (i * self.cell_size + (self.cell_size - cell_letter.get_rect().width) // 2,
                                     (lines.get_height() - cell_letter.get_rect().height) // 2))

            rows.blit(cell_number, ((rows.get_width() - cell_number.get_rect().width) // 2,
                                    i * self.cell_size + (self.cell_size - cell_letter.get_rect().height) // 2))
        return (rows, lines)

    def create_cells(self):
        sprite_group = pygame.sprite.Group()
        color_index = 1
        for y in range(self.qty_cells):
            for x in range(self.qty_cells):
                cell = Cell(color_index, self.cell_size, (x, y), LETTERS_NAME[x] + str(self.qty_cells - y))
                sprite_group.add(cell)
                color_index ^= True
            color_index ^= True
        return sprite_group

    def draw_cells_on_board(self, offset):
        for cell in self.all_cells:
            cell.rect.x += offset[0]
            cell.rect.y += offset[1]

    def setup(self):
        for j, row in enumerate(self.start_board):
            for i, field_value in enumerate(row):
                if field_value != '0':
                    piece = self.create_piece(field_value, (j, i))
                    self.all_pieces.add(piece)
        for piece in self.all_pieces:
            for cell in self.all_cells:
                if piece.field_name == cell.field_name:
                    piece.rect = cell.rect.copy()

    def create_piece(self, piece_symbol, table_coord):
        field_name = self.to_field_name(table_coord)
        piece_tuple = self.piece_types[piece_symbol]
        classname = globals()[piece_tuple[0]]
        return classname(self.cell_size, piece_tuple[1], field_name)

    def to_field_name(self, table_coord):
        return LETTERS_NAME[table_coord[1]] + str(self.qty_cells - table_coord[0])

    def get_cell(self, pos):
        for cell in self.all_cells:
            if cell.rect.collidepoint(pos):
                return cell
        return None

    def btn_down(self, position):
        self.pressed_cell = self.get_cell(position)
        self.unmark_cell(self.pressed_cell)
        self.dragged_piece = self.get_piece_on_cell(self.pressed_cell)
        if self.dragged_piece is not None:
            self.dragged_piece.rect.center = position
            dragged = Area(self.pressed_cell)
            self.all_areas.add(dragged)
            self.update_all()

    def btn_up(self, position):
        released_cell = self.get_cell(position)
        piece = self.get_piece_on_cell(released_cell)
        if (released_cell is not None) and (released_cell == self.pressed_cell):
            self.pick_cell(released_cell)
        if self.dragged_piece is not None:
            if (piece is not None) and (released_cell != self.pressed_cell):
                self.piece_del(piece)
            self.dragged_piece.move_to_cell(released_cell)
            dragged = Area(released_cell)
            self.all_areas.add(dragged)
            self.dragged_piece = None
        self.update_all()

    def get_piece_on_cell(self, cell):
        for piece in self.all_pieces:
            if piece.field_name == cell.field_name:
                return piece
        return None

    def drag(self, position):
        if self.dragged_piece is not None:
            self.dragged_piece.rect.center = position
            self.update_all()

    def update_all(self):
        self.all_cells.draw(self.screen)
        self.all_areas.draw(self.screen)
        self.all_pieces.draw(self.screen)
        pygame.display.update()

    def pick_cell(self, cell):
        self.unmark_cell(cell)
        piece = self.get_piece_on_cell(cell)
        if self.picked_piece is None:
            if piece is not None:
                pick = Area(cell)
                self.all_areas.add(pick)
                self.picked_piece = piece
        else:
            if piece is not None:
                self.piece_del(piece)
            self.picked_piece.move_to_cell(cell)
            moved = Area(cell)
            self.all_areas.add(moved)
            self.picked_piece = None

    def unmark_cell(self, cell):
        if self.picked_piece is None:
            self.all_areas.empty()

    def piece_del(self, deleting_piece):
        self.all_pieces.remove(deleting_piece)


class Area(pygame.sprite.Sprite):
    def __init__(self, cell):
        super().__init__()
        coords = (cell.rect.x, cell.rect.y)
        area_size = (cell.rect.width, cell.rect.height)
        self.image = pygame.Surface(area_size)
        self.image.fill(LIGHT_GREEN)
        self.rect = pygame.Rect(coords, area_size)
        self.field_name = cell.field_name


class Cell(pygame.sprite.Sprite):
    def __init__(self, color_index, size, coords, name):
        super().__init__()
        x, y = coords
        self.color = color_index
        self.field_name = name
        self.image = pygame.image.load(IMG_PATH + CELL_COLORS[color_index])
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x * size, y * size, size, size)
