"""HGSS Voltorb Flip Prediction"""
from dataclasses import dataclass
from enum import Enum
from rngs import MT

class Tile(Enum):
    """Tile data as stored in game"""
    NONE = 0
    MULTIPLIER1X = 1
    MULTIPLIER2X = 2
    MULTIPLIER3X = 3
    BOMB = 4

@dataclass
class BoardType:
    """Store data about board type"""
    bomb_count: int
    multiplier_2x_count: int
    multiplier_3x_count: int
    total_free_allowed: int
    row_col_free_allowed: int

class VoltorbFlip:
    """HGSS Voltorb Flip Prediction"""
    BOARD_DATA = [
        # bombs, 2x, 3x, total free, row/col free
        [
            [6,3,1,3,3],
            [6,0,3,2,2],
            [6,5,0,4,3],
            [6,2,2,3,3],
            [6,4,1,4,3],
            [6,3,1,3,3],
            [6,0,3,2,2],
            [6,5,0,4,3],
            [6,2,2,3,3],
            [6,4,1,4,3],
        ],
        [
            [7,1,3,3,2],
            [7,6,0,4,3],
            [7,3,2,3,2],
            [7,0,4,3,2],
            [7,5,1,4,3],
            [7,1,3,2,2],
            [7,6,0,3,3],
            [7,3,2,2,2],
            [7,0,4,2,2],
            [7,5,1,3,3],
        ],
        [
            [8,2,3,3,2],
            [8,7,0,4,3],
            [8,4,2,4,3],
            [8,1,4,3,2],
            [8,6,1,3,4],
            [8,2,3,2,2],
            [8,7,0,3,3],
            [8,4,2,3,3],
            [8,1,4,2,2],
            [8,6,1,3,3],
        ],
        [
            [8,3,3,3,4],
            [8,0,5,3,2],
            [10,8,0,5,4],
            [10,5,2,4,3],
            [10,2,4,4,3],
            [8,3,3,3,3],
            [8,0,5,2,2],
            [10,8,0,4,4],
            [10,5,2,3,3],
            [10,2,4,3,3],
        ],
        [
            [10,7,1,5,4],
            [10,4,3,4,3],
            [10,1,5,4,3],
            [10,9,0,5,4],
            [10,6,2,5,4],
            [10,7,1,4,4],
            [10,4,3,3,3],
            [10,1,5,3,3],
            [10,9,0,4,4],
            [10,6,2,4,4],
        ],
        [
            [10,3,4,4,3],
            [10,0,6,4,3],
            [10,8,1,5,4],
            [10,5,3,5,4],
            [10,2,5,4,3],
            [10,3,4,3,3],
            [10,0,6,3,3],
            [10,8,1,4,4],
            [10,5,3,4,4],
            [10,2,5,3,3],
        ],
        [
            [10,7,2,5,4],
            [10,4,4,5,4],
            [13,1,6,4,3],
            [13,9,1,6,5],
            [10,6,3,5,4],
            [10,7,2,4,4],
            [10,4,4,4,4],
            [13,1,6,3,3],
            [13,9,1,5,5],
            [10,6,3,4,4],
        ],
        [
            [10,0,7,4,3],
            [10,8,2,6,5],
            [10,5,4,5,4],
            [10,2,6,5,4],
            [10,7,3,6,5],
            [10,0,7,3,3],
            [10,8,2,5,5],
            [10,5,4,4,4],
            [10,2,6,4,4],
            [10,7,3,5,5],
        ],
    ]

    DISPLAY_VALUES = ["-", "1", "2", "3", "V"]

    def __init__(self, seed, level):
        self.rng = MT(seed)
        self.level = level
        self.board = [[Tile.NONE for _ in range(5)] for _ in range(5)]
        self.board_type = None

    def generate_board(self):
        """Generate full voltorb flip board"""
        self.board_type = (self.rng.next() % 100) // 10
        # arbitrary maximum tries set by the game
        for _ in range(1000):
            self.fill_in_board(Tile.MULTIPLIER1X, 25, False)
            self.fill_in_board(Tile.BOMB, self.board_type_data.bomb_count, True)
            self.fill_in_board(Tile.MULTIPLIER2X, self.board_type_data.multiplier_2x_count, True)
            self.fill_in_board(Tile.MULTIPLIER3X, self.board_type_data.multiplier_3x_count, True)
            if self.validate_board():
                break

    def fill_in_board(self, tile_type, tile_count, random_position):
        """Fill in board based on tile type, count of tile, and whether or not the x/y is random"""
        for i in range(tile_count):
            if random_position:
                valid_pos_chosen = False
                while not valid_pos_chosen:
                    pos = self.rng.next() % 25
                    if self.board[pos // 5][pos % 5] == Tile.MULTIPLIER1X:
                        self.board[pos // 5][pos % 5] = tile_type
                        valid_pos_chosen = True
            else:
                self.board[i // 5][i % 5] = tile_type

    def validate_board(self):
        """Validate that board matches free multiplier limits"""
        rows_free = [0 for _ in range(5)]
        cols_free = [0 for _ in range(5)]
        total_free = 0
        for y_pos in range(5):
            for x_pos in range(5):
                if self.board[y_pos][x_pos] in (Tile.MULTIPLIER2X, Tile.MULTIPLIER3X) \
                  and (Tile.BOMB not in self.rows[y_pos] or Tile.BOMB not in self.cols[x_pos]):
                    rows_free[y_pos] += 1
                    cols_free[x_pos] += 1
                    total_free += 1
                    if total_free >= self.board_type_data.total_free_allowed \
                      or rows_free[y_pos] >= self.board_type_data.row_col_free_allowed \
                      or cols_free[x_pos] >= self.board_type_data.row_col_free_allowed:
                        return False
        return True

    @property
    def total_advance_causing_tiles(self):
        """Get amount of tiles that cause advances when clicked"""
        total = 0
        for y_pos in range(5):
            for x_pos in range(5):
                if self.board[y_pos][x_pos] != Tile.BOMB \
                  and Tile.BOMB in self.rows[y_pos] \
                  and Tile.BOMB in self.cols[x_pos]:
                    total += 1
        return total

    @property
    def display_board(self):
        """Display board in human readable format"""
        return "\n".join(
            " ".join(
                    self.DISPLAY_VALUES[tile.value] for tile in row
                ) for row in self.board
            )

    @property
    def board_types(self):
        """Get list of board types from level"""
        return self.BOARD_DATA[self.level - 1]

    @property
    def board_type_data(self):
        """Get board data from board type and level"""
        return BoardType(*self.board_types[self.board_type])

    @property
    def rows(self):
        """Get list of rows (copy of self.board)"""
        return self.board.copy()

    @property
    def cols(self):
        """Get list of cols"""
        return [[row[i] for row in self.rows] for i in range(5)]

if __name__ == "__main__":
    game = VoltorbFlip(0xCB130344, 1)
    game.generate_board()
    print(game.display_board)
    game.rng.advance(game.total_advance_causing_tiles)
