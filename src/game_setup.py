import numpy as np
from numpy.random import Generator
from typing import Tuple, Dict, List

# --- CONSTANTS ---
BOARD_SIZE: Tuple[int, int] = (10, 10)
SHIP_CONFIG: Dict[int, int] = {
    5: 1,  # Carrier
    4: 1,  # Battleship
    3: 2,  # Destroyer/Cruiser
    2: 1  # Submarine
}


def is_space_free(
        board: np.ndarray,
        row: int,
        col: int,
        length: int,
        horizontal: bool
) -> bool:
    """
    Checks if a ship can be placed at the given position with a 1-cell safety buffer.
    """
    rows, cols = BOARD_SIZE

    if horizontal:
        if col + length > cols:
            return False
        for c in range(col, col + length):
            for r_off in [-1, 0, 1]:
                for c_off in [-1, 0, 1]:
                    nr, nc = row + r_off, c + c_off
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr, nc] != 0:
                        return False
    else:  # Vertical
        if row + length > rows:
            return False
        for r in range(row, row + length):
            for r_off in [-1, 0, 1]:
                for c_off in [-1, 0, 1]:
                    nr, nc = r + r_off, col + c_off
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr, nc] != 0:
                        return False
    return True


def create_new_board(rng: Generator) -> np.ndarray:
    """
    Initializes a board and places ships.
    If placement fails due to a 'tight' random configuration,
    it restarts the entire board creation to ensure robustness.
    """
    while True:
        board: np.ndarray = np.zeros(BOARD_SIZE, dtype=int)
        rows, cols = BOARD_SIZE

        ship_lengths: List[int] = []
        for length, count in SHIP_CONFIG.items():
            ship_lengths.extend([length] * count)

        # Randomize the order in which ships are placed
        ship_lengths = rng.permutation(ship_lengths)
        all_placed_successfully = True

        for length in ship_lengths:
            placed = False
            attempts = 0
            # Try placing the specific ship up to 500 times
            while not placed and attempts < 500:
                attempts += 1
                is_horizontal = rng.choice([True, False])

                if is_horizontal:
                    max_r, max_c = rows - 1, cols - length
                else:
                    max_r, max_c = rows - length, cols - 1

                r_start = rng.integers(0, max_r + 1)
                c_start = rng.integers(0, max_c + 1)

                if is_space_free(board, r_start, c_start, length, is_horizontal):
                    if is_horizontal:
                        board[r_start, c_start: c_start + length] = length
                    else:
                        board[r_start: r_start + length, c_start] = length
                    placed = True

            if not placed:
                # If a ship couldn't be placed, break and restart the whole board
                all_placed_successfully = False
                break

        if all_placed_successfully:
            return board