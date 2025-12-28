import numpy as np
from numpy.random import Generator
from .game_setup import create_new_board, SHIP_CONFIG, BOARD_SIZE


def run_random_simulation(rng: Generator) -> int:
    """
    Simulates a game using a purely random shooting strategy.
    Receives a ready-to-use Generator via dependency injection.
    """
    board = create_new_board(rng=rng)

    total_targets = np.sum([l * count for l, count in SHIP_CONFIG.items()])
    shots_fired, hits_count = 0, 0

    rows, cols = BOARD_SIZE
    coordinates = [(r, c) for r in range(rows) for c in range(cols)]

    # Shuffle the coordinates list using the injected generator
    coordinates = list(rng.permutation(coordinates))

    while hits_count < total_targets:
        if not coordinates: break
        r, c = coordinates.pop()
        shots_fired += 1

        if board[r, c] > 0:
            hits_count += 1

    return shots_fired